import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, time
import plotly.express as px
import plotly.graph_objects as go
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
import io
import json
import math
from collections import defaultdict

# Enhanced Data Models for NEP 2020
@dataclass
class Course:
    id: str
    name: str
    credits: int
    course_type: str  # Major/Minor, Elective, Practical/Lab/Studio, School_Internship, Fieldwork, AECC/VAC
    total_duration_hours: int  # Total hours for the entire semester
    faculty_expertise_required: str
    room_type_required: str  # classroom, lab, hall, none for internship
    max_students: int
    semester: int
    is_elective: bool = False

@dataclass
class Faculty:
    id: str
    name: str
    expertise: str  # Single expertise area
    max_load_per_week: int
    availability: Dict[str, List[int]]  # day -> available_period_numbers

@dataclass
class Room:
    id: str
    name: str
    capacity: int
    room_type: str  # classroom, lab, hall
    equipment: List[str]

@dataclass
class Student:
    id: str
    name: str
    semester: int
    enrolled_courses: List[str]
    course_groups: Dict[str, int] = field(default_factory=dict)  # course_id -> group_num

@dataclass
class TimeSlot:
    id: str
    day: str
    period_number: int  # 1-7 periods per day
    start_time: str
    end_time: str
    duration_minutes: int = 60

@dataclass
class Gene:
    course_id: str
    timeslot_id: str
    faculty_id: str
    room_id: str
    student_group: int = 1  # For splitting

class TimetableChromosome:
    def __init__(self, genes: List[Gene]):
        self.genes = genes
        self.fitness = 0.0
        self.hard_violations = 0
        self.soft_violations = 0
        self.penalty_score = 0
        self.reward_score = 0

class EnhancedGeneticTimetableGenerator:
    def __init__(self):
        self.courses = []
        self.faculty = []
        self.rooms = []
        self.students = []
        self.timeslots = []
        
        # Algorithm parameters
        self.population_size = 100
        self.generations = 500
        self.mutation_rate = 0.1
        self.crossover_rate = 0.8
        self.elite_size = 10
        
        # NEP 2020 Constants
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        self.WORKING_DAYS_PER_WEEK = 6
        self.PERIODS_PER_DAY = 7
        self.PERIOD_DURATION_MINUTES = 60
        self.LUNCH_BREAK_AFTER_PERIOD = 3
        self.LUNCH_BREAK_DURATION = 30
        self.TOTAL_SEMESTER_WEEKS = 16  # Approx 96 days / 6 = 16 weeks
        self.WORKING_DAYS_IN_SEMESTER = 96
        self.MAX_TUTORIAL_HOURS_PER_WEEK = 40
        self.MIN_SEMESTER_CREDITS = 22
        self.MAX_SEMESTER_CREDITS = 24
        
        # Credit to hours conversion (per week)
        self.CREDIT_HOURS_MAPPING = {
            'Major': 4,
            'Minor': 2,
            'Elective': 2,
            'Practical': 3,
            'Lab': 3,
            'Studio': 3,
            'Fieldwork': 3,
            'School_Internship': 7,  # Adjusted to fit full day ~7 hours
            'AECC/VAC': 2,
        }

    def load_data_from_ui(self, courses_df, faculty_df, rooms_df, students_df):
        """Load data from Streamlit uploaded files"""
        try:
            # Clear existing data
            self.courses.clear()
            self.faculty.clear()
            self.rooms.clear()
            self.students.clear()
            
            # Generate time slots
            self._generate_time_slots()
            
            # Load courses
            for _, row in courses_df.iterrows():
                course = Course(
                    id=str(row['Course_ID']),
                    name=str(row['Course_Name']),
                    credits=int(row['Credits']),
                    course_type=str(row['Course_Type']),
                    total_duration_hours=int(row['Total_Duration_Hours']),
                    faculty_expertise_required=str(row['Faculty_Expertise_Required']),
                    room_type_required=str(row['Room_Type_Required']),
                    max_students=int(row['Max_Students']),
                    semester=int(row['Semester']),
                    is_elective=bool(row.get('Is_Elective', False))
                )
                self.courses.append(course)
            
            # Load faculty
            for _, row in faculty_df.iterrows():
                try:
                    availability_str = str(row.get('Availability', '{}'))
                    availability = json.loads(availability_str)
                    # Ensure availability is dict day -> list[int]
                    for day in self.days:
                        if day not in availability:
                            availability[day] = list(range(1, 8))
                except:
                    availability = {day: list(range(1, 8)) for day in self.days}
                
                faculty = Faculty(
                    id=str(row['Faculty_ID']),
                    name=str(row['Faculty_Name']),
                    expertise=str(row['Expertise']),
                    max_load_per_week=int(row['Max_Load_Per_Week']),
                    availability=availability
                )
                self.faculty.append(faculty)
            
            # Load rooms
            for _, row in rooms_df.iterrows():
                equipment_str = str(row.get('Equipment', ''))
                equipment = [e.strip() for e in equipment_str.split(',') if e.strip()] if equipment_str else []
                
                room = Room(
                    id=str(row['Room_ID']),
                    name=str(row['Room_Name']),
                    capacity=int(row['Capacity']),
                    room_type=str(row['Room_Type']),
                    equipment=equipment
                )
                self.rooms.append(room)
            
            # Load students
            for _, row in students_df.iterrows():
                enrolled_str = str(row.get('Enrolled_Courses', ''))
                enrolled = [c.strip() for c in enrolled_str.split(',') if c.strip()] if enrolled_str else []
                
                student = Student(
                    id=str(row['Student_ID']),
                    name=str(row['Student_Name']),
                    semester=int(row['Semester']),
                    enrolled_courses=enrolled,
                    course_groups={}
                )
                self.students.append(student)
            
            # Assign groups for courses that need splitting
            self._assign_student_groups()
            
        except Exception as e:
            st.error(f"Error loading data: {e}")
            raise

    def _assign_student_groups(self):
        """Assign student groups for courses requiring splitting"""
        try:
            for course in self.courses:
                enrolled_students = [s for s in self.students if course.id in s.enrolled_courses]
                if not enrolled_students:
                    continue
                
                suitable_rooms = [r for r in self.rooms if r.room_type == course.room_type_required and course.room_type_required != 'none']
                max_cap = max([r.capacity for r in suitable_rooms], default=course.max_students)
                groups_needed = math.ceil(len(enrolled_students) / max_cap)
                
                if groups_needed > 1:
                    enrolled_list = sorted(enrolled_students, key=lambda s: s.id)
                    for i, student in enumerate(enrolled_list):
                        group = (i % groups_needed) + 1
                        student.course_groups[course.id] = group
        except Exception as e:
            st.warning(f"Error assigning groups: {e}")

    def _generate_time_slots(self):
        """Generate time slots for 6 working days with 7 periods each"""
        self.timeslots.clear()
        
        # Period timings (7 periods with lunch break after 3rd period)
        period_times = [
            ('09:00', '10:00'),  # Period 1
            ('10:00', '11:00'),  # Period 2
            ('11:00', '12:00'),  # Period 3
            ('12:30', '13:30'),  # Period 4 (after lunch)
            ('13:30', '14:30'),  # Period 5
            ('14:30', '15:30'),  # Period 6
            ('15:30', '16:30'),  # Period 7
        ]
        
        slot_id = 1
        for day in self.days:
            for period_num, (start, end) in enumerate(period_times, 1):
                timeslot = TimeSlot(
                    id=f'T{slot_id:03d}',
                    day=day,
                    period_number=period_num,
                    start_time=start,
                    end_time=end,
                    duration_minutes=60
                )
                self.timeslots.append(timeslot)
                slot_id += 1

    def _calculate_required_sessions_per_week(self, course: Course) -> int:
        """Calculate how many sessions per week a course needs"""
        try:
            if course.course_type == 'School_Internship':
                return 7  # Full day
            
            course_type = course.course_type
            hours_per_week = course.credits * self.CREDIT_HOURS_MAPPING.get(course_type, 2)
            sessions_per_week = math.ceil(hours_per_week)
            
            # Ensure minimum constraint: course_duration / no_of_weeks
            min_sessions_per_week = math.ceil(course.total_duration_hours / self.TOTAL_SEMESTER_WEEKS)
            
            return max(sessions_per_week, min_sessions_per_week)
        except:
            return 1  # Fallback

    def _calculate_student_groups(self, course: Course, enrolled_students: List[Student], suitable_rooms: List[Room]) -> int:
        """Calculate number of student groups needed"""
        try:
            if course.room_type_required == 'none':
                return 1
            max_room_capacity = max([r.capacity for r in suitable_rooms]) if suitable_rooms else course.max_students
            effective_capacity = min(course.max_students, max_room_capacity)
            return math.ceil(len(enrolled_students) / effective_capacity) if effective_capacity > 0 else 1
        except:
            return 1

    def create_random_chromosome(self) -> TimetableChromosome:
        """Create a random chromosome with proper NEP 2020 constraints"""
        try:
            genes = []
            
            # First, schedule internships (full day blocks)
            internship_courses = [c for c in self.courses if c.course_type == 'School_Internship']
            for course in internship_courses:
                suitable_faculty = [f for f in self.faculty if f.expertise == course.faculty_expertise_required]
                if not suitable_faculty:
                    suitable_faculty = self.faculty
                faculty = random.choice(suitable_faculty)
                
                # Choose one random day for full schedule
                day = random.choice(self.days)
                day_timeslots = [t for t in self.timeslots if t.day == day]
                
                # No room for internship
                room_id = ''
                
                for timeslot in day_timeslots:
                    # Check faculty availability
                    if timeslot.period_number in faculty.availability.get(timeslot.day, []):
                        gene = Gene(
                            course_id=course.id,
                            timeslot_id=timeslot.id,
                            faculty_id=faculty.id,
                            room_id=room_id,
                            student_group=1
                        )
                        genes.append(gene)
            
            # Now schedule other courses
            for course in [c for c in self.courses if c.course_type != 'School_Internship']:
                enrolled_students = [s for s in self.students if course.id in s.enrolled_courses]
                sessions_per_week = self._calculate_required_sessions_per_week(course)
                
                # Find suitable faculty
                suitable_faculty = [f for f in self.faculty if f.expertise == course.faculty_expertise_required]
                if not suitable_faculty:
                    suitable_faculty = self.faculty
                
                # Find suitable rooms
                suitable_rooms = [r for r in self.rooms if r.room_type == course.room_type_required]
                if not suitable_rooms and course.room_type_required != 'none':
                    suitable_rooms = self.rooms
                
                groups_needed = self._calculate_student_groups(course, enrolled_students, suitable_rooms)
                
                # Generate genes for this course
                for session in range(sessions_per_week):
                    timeslot = random.choice(self.timeslots)
                    
                    for group_num in range(1, groups_needed + 1):
                        # Choose available faculty
                        available_faculty = [
                            f for f in suitable_faculty 
                            if timeslot.day in f.availability and timeslot.period_number in f.availability[timeslot.day]
                        ]
                        if not available_faculty:
                            available_faculty = suitable_faculty
                        faculty = random.choice(available_faculty)
                        
                        # Choose suitable room with capacity
                        group_students = [
                            s for s in enrolled_students if s.course_groups.get(course.id, 1) == group_num
                        ]
                        suitable_for_group = [
                            r for r in suitable_rooms if r.capacity >= len(group_students)
                        ]
                        if not suitable_for_group:
                            suitable_for_group = suitable_rooms
                        room = random.choice(suitable_for_group) if suitable_for_group else None
                        room_id = room.id if room else ''
                        
                        gene = Gene(
                            course_id=course.id,
                            timeslot_id=timeslot.id,
                            faculty_id=faculty.id,
                            room_id=room_id,
                            student_group=group_num
                        )
                        genes.append(gene)
            
            return TimetableChromosome(genes)
        except Exception as e:
            st.warning(f"Error creating chromosome: {e}")
            return TimetableChromosome([])

    def calculate_fitness(self, chromosome: TimetableChromosome) -> float:
        """Enhanced fitness calculation with NEP 2020 compliance"""
        try:
            penalty = 0
            reward = 0
            
            # Create lookup dictionaries
            course_dict = {c.id: c for c in self.courses}
            faculty_dict = {f.id: f for f in self.faculty}
            room_dict = {r.id: r for r in self.rooms}
            timeslot_dict = {t.id: t for t in self.timeslots}
            
            # Tracking structures
            faculty_schedule = {f.id: {} for f in self.faculty}
            room_schedule = {r.id: {} for r in self.rooms}
            student_schedules = {s.id: {} for s in self.students}
            
            # HARD CONSTRAINTS
            for gene in chromosome.genes:
                course = course_dict.get(gene.course_id)
                faculty = faculty_dict.get(gene.faculty_id)
                room = room_dict.get(gene.room_id) if gene.room_id else None
                timeslot = timeslot_dict.get(gene.timeslot_id)
                
                if not all([course, faculty, timeslot]):
                    penalty += 100000
                    continue
                
                # Hard 8: Faculty availability
                if timeslot.period_number not in faculty.availability.get(timeslot.day, []):
                    penalty += 100000
                
                # Hard 3: Faculty overlap
                if gene.timeslot_id in faculty_schedule[gene.faculty_id]:
                    penalty += 100000
                else:
                    faculty_schedule[gene.faculty_id][gene.timeslot_id] = gene.course_id
                
                # Hard 3: Room overlap (if room assigned)
                if room and gene.timeslot_id in room_schedule[gene.room_id]:
                    penalty += 100000
                elif room:
                    room_schedule[gene.room_id][gene.timeslot_id] = gene.course_id
                
                # Hard 4,2: Student clash and capacity
                group_students = [
                    s for s in self.students 
                    if gene.course_id in s.enrolled_courses and s.course_groups.get(gene.course_id, 1) == gene.student_group
                ]
                for student in group_students:
                    if gene.timeslot_id in student_schedules[student.id]:
                        penalty += 100000
                    else:
                        student_schedules[student.id][gene.timeslot_id] = gene.course_id
                
                if room and len(group_students) > room.capacity:
                    penalty += 100000
                
                # Hard 5,9,10: Expertise and room type
                if faculty.expertise != course.faculty_expertise_required:
                    penalty += 50000
                if room and room.room_type != course.room_type_required:
                    penalty += 50000
            
            # Hard 6: Credit limits (per student, strictly 22-24)
            for student in self.students:
                student_credits = sum(course_dict[c].credits for c in student.enrolled_courses if c in course_dict)
                if student_credits < self.MIN_SEMESTER_CREDITS or student_credits > self.MAX_SEMESTER_CREDITS:
                    penalty += 100000
            
            # Hard 13: All slots occupied
            used_slots = set(gene.timeslot_id for gene in chromosome.genes)
            if len(used_slots) < len(self.timeslots):
                penalty += (len(self.timeslots) - len(used_slots)) * 10000
            
            # Hard 1: Total tutorial hours <=40/week (unique occupied slots <=40, but 42 max, approx)
            if len(used_slots) > self.MAX_TUTORIAL_HOURS_PER_WEEK:
                penalty += (len(used_slots) - self.MAX_TUTORIAL_HOURS_PER_WEEK) * 10000
            
            # SOFT CONSTRAINTS
            # Soft 1: Faculty workload 16-20 hours/week
            for fid, schedule in faculty_schedule.items():
                weekly_hours = len(schedule)
                if weekly_hours > faculty_dict[fid].max_load_per_week:
                    penalty += (weekly_hours - faculty_dict[fid].max_load_per_week) * 10
                elif weekly_hours < 16:
                    penalty += (16 - weekly_hours) * 10
                else:
                    reward += 50
            
            # Soft 2: Avoid >3 consecutive for students
            for sid, schedule in student_schedules.items():
                daily_schedules = defaultdict(list)
                for tsid in schedule:
                    ts = timeslot_dict.get(tsid)
                    if ts:
                        daily_schedules[ts.day].append(ts.period_number)
                
                for day, periods in daily_schedules.items():
                    if not periods:
                        continue
                    periods.sort()
                    consecutive = 1
                    max_consec = 1
                    for i in range(1, len(periods)):
                        if periods[i] == periods[i-1] + 1:
                            consecutive += 1
                            max_consec = max(max_consec, consecutive)
                        else:
                            consecutive = 1
                    if max_consec > 3:
                        penalty += (max_consec - 3) * 20
                    else:
                        reward += 30
            
            # Soft 3: Theory in morning
            for gene in chromosome.genes:
                course = course_dict.get(gene.course_id)
                ts = timeslot_dict.get(gene.timeslot_id)
                if course and ts and course.course_type in ['Major', 'Minor', 'Elective', 'AECC/VAC']:
                    if ts.period_number <= 3:
                        reward += 20
                    else:
                        penalty += 10
            
            # Soft 5: Avoid monotony (same period every day)
            course_periods = defaultdict(list)
            for gene in chromosome.genes:
                ts = timeslot_dict.get(gene.timeslot_id)
                if ts:
                    course_periods[gene.course_id].append(ts.period_number)
            
            for cid, periods in course_periods.items():
                if len(periods) < 2:
                    continue
                period_counts = defaultdict(int)
                for p in periods:
                    period_counts[p] += 1
                max_same = max(period_counts.values())
                if max_same > len(self.days) // 2:
                    penalty += (max_same - 1) * 5
            
            # Calculate final fitness
            total_violations = penalty - reward
            
            max_possible_penalty = 100000 * max(len(chromosome.genes), 1) * 2
            fitness = max(0, 1 - (total_violations / max_possible_penalty))
            
            chromosome.fitness = fitness
            chromosome.penalty_score = penalty
            chromosome.reward_score = reward
            chromosome.hard_violations = penalty // 10000 if penalty >= 10000 else 0  # Adjusted threshold
            chromosome.soft_violations = max(0, int(penalty - chromosome.hard_violations * 10000))
            
            return fitness
        except Exception as e:
            st.warning(f"Error in fitness calculation: {e}")
            return 0.0

    def selection(self, population: List[TimetableChromosome]) -> List[TimetableChromosome]:
        """Tournament selection"""
        try:
            selected = []
            tournament_size = min(5, len(population))
            
            for _ in range(len(population)):
                tournament = random.sample(population, tournament_size)
                winner = max(tournament, key=lambda x: x.fitness)
                selected.append(winner)
            
            return selected
        except:
            return population[:10] if population else []

    def crossover(self, parent1: TimetableChromosome, parent2: TimetableChromosome) -> Tuple[TimetableChromosome, TimetableChromosome]:
        """Single-point crossover with error handling"""
        try:
            if random.random() > self.crossover_rate or min(len(parent1.genes), len(parent2.genes)) < 2:
                return parent1, parent2
            
            min_length = min(len(parent1.genes), len(parent2.genes))
            crossover_point = random.randint(1, min_length - 1)
            
            child1_genes = parent1.genes[:crossover_point] + parent2.genes[crossover_point:]
            child2_genes = parent2.genes[:crossover_point] + parent1.genes[crossover_point:]
            
            return TimetableChromosome(child1_genes), TimetableChromosome(child2_genes)
        except:
            return parent1, parent2

    def mutate(self, chromosome: TimetableChromosome) -> TimetableChromosome:
        """Enhanced mutation with error handling"""
        try:
            mutated_genes = chromosome.genes.copy()
            
            for i, gene in enumerate(mutated_genes):
                if random.random() < self.mutation_rate:
                    course = next((c for c in self.courses if c.id == gene.course_id), None)
                    if not course:
                        continue
                    
                    mutation_type = random.choice(['timeslot', 'room', 'faculty'])
                    
                    if mutation_type == 'timeslot' and self.timeslots:
                        gene.timeslot_id = random.choice(self.timeslots).id
                    
                    elif mutation_type == 'room' and course.room_type_required != 'none':
                        suitable_rooms = [r for r in self.rooms if r.room_type == course.room_type_required]
                        if suitable_rooms:
                            gene.room_id = random.choice(suitable_rooms).id
                    
                    elif mutation_type == 'faculty':
                        suitable_faculty = [f for f in self.faculty if f.expertise == course.faculty_expertise_required]
                        if suitable_faculty:
                            gene.faculty_id = random.choice(suitable_faculty).id
            
            return TimetableChromosome(mutated_genes)
        except:
            return chromosome

    def evolve(self, progress_callback=None) -> Tuple[TimetableChromosome, List[float]]:
        """Enhanced evolution with error handling"""
        try:
            # Initialize population
            population = []
            for _ in range(self.population_size):
                chromosome = self.create_random_chromosome()
                if chromosome.genes:  # Only add valid
                    self.calculate_fitness(chromosome)
                    population.append(chromosome)
            
            if not population:
                raise Exception("Failed to create initial population")
            
            best_fitness_history = []
            
            for generation in range(self.generations):
                population.sort(key=lambda x: x.fitness, reverse=True)
                
                best_fitness = population[0].fitness
                best_fitness_history.append(best_fitness)
                
                if progress_callback:
                    hard_violations = population[0].hard_violations
                    progress_callback(generation, self.generations, best_fitness, hard_violations)
                
                if population[0].hard_violations == 0 and population[0].fitness > 0.95:
                    break
                
                # Elitism
                new_population = population[:self.elite_size]
                
                # Generate new
                selected = self.selection(population)
                i = 0
                while len(new_population) < self.population_size and i < len(selected) - 1:
                    child1, child2 = self.crossover(selected[i], selected[i+1])
                    child1 = self.mutate(child1)
                    child2 = self.mutate(child2)
                    self.calculate_fitness(child1)
                    self.calculate_fitness(child2)
                    new_population.extend([child1, child2])
                    i += 2
                
                population = new_population[:self.population_size]
            
            population.sort(key=lambda x: x.fitness, reverse=True)
            return population[0], best_fitness_history
        except Exception as e:
            st.error(f"Evolution error: {e}")
            raise

def create_nep2020_sample_data():
    """Create NEP 2020 compliant sample data for B.Sc+B.Ed 7th Semester"""
    try:
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        full_availability = {d: list(range(1, 8)) for d in days}
        
        # Courses for 7th sem B.Sc+B.Ed, total 23 credits
        courses_data = {
            'Course_ID': ['CAP701', 'FOUND701', 'PED701', 'MAJ701', 'ELE702', 'PRAC701', 'AE701'],
            'Course_Name': [
                'Capstone Teaching Project / Internship', 'Advanced Foundations & Ethics in Education',
                'Content & Pedagogy - Advanced (Major)', 'Major: Capstone Elective / Seminar',
                'Alternative Elective / Seminar', 'Science Practical Lab', 'AE & VAC / Community Engagement Project'
            ],
            'Credits': [8, 3, 4, 3, 3, 3, 2],
            'Course_Type': [
                'School_Internship', 'Minor', 'Major', 'Elective', 'Elective',
                'Practical', 'AECC/VAC'
            ],
            'Total_Duration_Hours': [105, 90, 240, 90, 90, 135, 60],  # credits * hours_per_credit * 16 weeks
            'Faculty_Expertise_Required': [
                'Education', 'Education', 'Pedagogy', 'Disciplinary', 'Disciplinary',
                'Science', 'General'
            ],
            'Room_Type_Required': [
                'none', 'classroom', 'classroom', 'classroom', 'classroom',
                'lab', 'hall'
            ],
            'Max_Students': [100, 100, 100, 40, 40, 25, 100],
            'Semester': [7] * 7,
            'Is_Elective': [False, False, False, True, True, False, False]
        }
        
        # Faculty with sufficient numbers
        faculty_names = [
            'Dr. A Sharma', 'Dr. B Patel', 'Prof. C Kumar', 'Dr. D Singh', 'Dr. E Gupta',
            'Prof. F Verma', 'Dr. G Jain', 'Prof. H Agarwal', 'Dr. I Mishra', 'Prof. J Tiwari',
            'Dr. K Rao', 'Prof. L Mehta', 'Dr. M Bose', 'Prof. N Desai', 'Dr. O Khan'
        ]
        expertise = [
            'Education', 'Education', 'Education', 'Pedagogy', 'Pedagogy',
            'Disciplinary', 'Disciplinary', 'Disciplinary', 'Science', 'Science',
            'Science', 'General', 'General', 'General', 'General'
        ]
        faculty_data = {
            'Faculty_ID': [f'F{i:03d}' for i in range(1, 16)],
            'Faculty_Name': faculty_names,
            'Expertise': expertise,
            'Max_Load_Per_Week': [20] * 15,
            'Availability': [json.dumps(full_availability) for _ in range(15)]
        }
        
        # Rooms: only classroom, lab, hall with sufficient capacity
        rooms_data = {
            'Room_ID': ['C001', 'C002', 'C003', 'C004', 'C005', 'L001', 'L002', 'L003', 'H001', 'H002'],
            'Room_Name': [
                'Classroom 1', 'Classroom 2', 'Classroom 3', 'Classroom 4', 'Classroom 5',
                'Lab 1', 'Lab 2', 'Lab 3', 'Hall 1', 'Hall 2'
            ],
            'Capacity': [60, 50, 70, 40, 55, 25, 30, 20, 80, 100],
            'Room_Type': [
                'classroom', 'classroom', 'classroom', 'classroom', 'classroom',
                'lab', 'lab', 'lab', 'hall', 'hall'
            ],
            'Equipment': [
                'Projector,Whiteboard', 'Smart Board', 'Projector', 'Whiteboard', 'Audio System',
                'Lab Equipment', 'Computers', 'Chem Lab', 'Large Screen', 'Projector'
            ]
        }
        
        # Students: 100 students, enrolled in core + practical + one elective (split for MAJ701)
        credit_lookup = {courses_data['Course_ID'][i]: courses_data['Credits'][i] for i in range(len(courses_data['Course_ID']))}
        students_data = {
            'Student_ID': [f'S{i:03d}' for i in range(1, 101)],
            'Student_Name': [f'Student {i}' for i in range(1, 101)],
            'Semester': [7] * 100,
            'Enrolled_Courses': []
        }
        
        core_courses = 'CAP701,FOUND701,PED701,PRAC701,AE701'  # 8+3+4+3+2=20
        for i in range(100):
            if i < 60:  # Split: 60 in MAJ701 (needs 2 groups, cap 40)
                elective = 'MAJ701'
            else:
                elective = 'ELE702'
            courses = f"{core_courses},{elective}"  # Total 23 credits
            students_data['Enrolled_Courses'].append(courses)
        
        return (
            pd.DataFrame(courses_data),
            pd.DataFrame(faculty_data),
            pd.DataFrame(rooms_data),
            pd.DataFrame(students_data)
        )
    except Exception as e:
        st.error(f"Error creating sample data: {e}")
        raise

def display_enhanced_timetable(chromosome: TimetableChromosome, generator: EnhancedGeneticTimetableGenerator):
    """Display timetable in the requested format with comprehensive error handling"""
    try:
        if not chromosome or not chromosome.genes:
            st.error("No timetable data to display")
            return
        
        # Create lookup dictionaries
        course_dict = {c.id: c for c in generator.courses}
        faculty_dict = {f.id: f for f in generator.faculty}
        room_dict = {r.id: r for r in generator.rooms}
        timeslot_dict = {t.id: t for t in generator.timeslots}
        
        # Create timetable matrix as lists
        periods = [
            'Period 1\n(09:00-10:00)', 'Period 2\n(10:00-11:00)', 'Period 3\n(11:00-12:00)',
            'LUNCH BREAK\n(12:00-12:30)', 'Period 4\n(12:30-13:30)', 'Period 5\n(13:30-14:30)', 
            'Period 6\n(14:30-15:30)', 'Period 7\n(15:30-16:30)'
        ]
        timetable_matrix = {day: [[] for _ in range(len(periods))] for day in generator.days}
        
        # Collect genes per cell
        for gene in chromosome.genes:
            course = course_dict.get(gene.course_id)
            faculty = faculty_dict.get(gene.faculty_id)
            room = room_dict.get(gene.room_id) if gene.room_id else None
            timeslot = timeslot_dict.get(gene.timeslot_id)
            
            if all([course, faculty, timeslot]):
                day = timeslot.day
                period_idx = timeslot.period_number - 1
                if period_idx >= 3:
                    period_idx += 1
                
                if 0 <= period_idx < len(periods) and day in timetable_matrix:
                    content = {
                        'course': course.name,
                        'course_id': course.id,
                        'is_elective': course.is_elective,
                        'room': room.name if room else 'Off-campus',
                        'faculty': faculty.name,
                        'group': gene.student_group
                    }
                    timetable_matrix[day][period_idx].append(content)
        
        # Format cells
        formatted_matrix = {}
        for day, cells in timetable_matrix.items():
            formatted_day = []
            for cell_list in cells:
                if not cell_list:
                    formatted_day.append('')
                    continue
                
                if len(cell_list) == 1 and not cell_list[0]['is_elective']:
                    content = cell_list[0]
                    fmt = f"{content['course']}\n{content['room']}\n{content['faculty']}"
                    if content['group'] > 1:
                        fmt += f"\nGroup {content['group']}"
                    formatted_day.append(fmt)
                else:
                    # Group by course_id
                    course_groups = defaultdict(list)
                    for content in cell_list:
                        course_groups[content['course_id']].append((
                            content['room'], content['faculty'], content['group']
                        ))
                    
                    formatted_entries = []
                    for cid, group_list in course_groups.items():
                        cname = next(c['course'] for c in cell_list if c['course_id'] == cid)
                        if len(group_list) > 1:  # Split
                            opts = ', '.join(f"{r}, {f}" for r, f, g in group_list)
                            formatted_entries.append(f"{cname} ({opts})")
                        else:
                            r, f, g = group_list[0]
                            formatted_entries.append(f"{cname} ({r}, {f})")
                    
                    formatted_day.append(' / '.join(formatted_entries))
            
            formatted_matrix[day] = formatted_day
        
        # Create DataFrame
        timetable_df = pd.DataFrame(formatted_matrix, index=periods)
        
        # Display summary
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Classes", len(chromosome.genes))
        with col2:
            st.metric("Hard Violations", chromosome.hard_violations)
        with col3:
            st.metric("Soft Violations", chromosome.soft_violations)
        with col4:
            st.metric("Fitness Score", f"{chromosome.fitness:.3f}")
        with col5:
            total_credits = sum(c.credits for c in generator.courses)
            st.metric("Total Credits", total_credits)
        
        st.subheader("📅 Weekly Timetable")
        st.dataframe(timetable_df, use_container_width=True, height=400)
        
        # Compliance check
        st.subheader("📊 NEP 2020 Compliance Check")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Credit Distribution:**")
            credit_dist = defaultdict(int)
            for course in generator.courses:
                credit_dist[course.course_type] += course.credits
            credit_df = pd.DataFrame(list(credit_dist.items()), columns=['Type', 'Credits'])
            st.dataframe(credit_df)
        
        with col2:
            st.write("**Faculty Workload:**")
            faculty_load = defaultdict(int)
            for gene in chromosome.genes:
                faculty_load[gene.faculty_id] += 1
            load_data = [
                {
                    'Faculty': faculty_dict.get(fid, {'name': f'Unknown {fid}'}).name,
                    'Hours': hours,
                    'Status': 'Optimal' if 16 <= hours <= 20 else 'Issue'
                }
                for fid, hours in faculty_load.items()
            ]
            load_df = pd.DataFrame(load_data)
            st.dataframe(load_df)
        
        if chromosome.hard_violations == 0:
            st.success("✅ All hard constraints satisfied!")
        else:
            st.warning("⚠️ Some hard constraints violated.")
        
        # Exports and viz similar to original, omitted for brevity
        st.subheader("📁 Export")
        csv = timetable_df.to_csv()
        st.download_button("CSV", csv, "timetable.csv")
        
    except Exception as e:
        st.error(f"Display error: {e}")

def main():
    st.set_page_config(page_title="NEP 2020 Timetable", layout="wide")
    st.title("🎓 NEP 2020 Timetable Generator - B.Sc+B.Ed 7th Sem")
    
    with st.sidebar:
        st.header("Config")
        population_size = st.slider("Population", 50, 200, 100)
        generations = st.slider("Generations", 100, 1000, 500)
        use_sample = st.checkbox("Sample Data", True)
    
    generator = EnhancedGeneticTimetableGenerator()
    generator.population_size = population_size
    generator.generations = generations
    
    if use_sample:
        courses_df, faculty_df, rooms_df, students_df = create_nep2020_sample_data()
        generator.load_data_from_ui(courses_df, faculty_df, rooms_df, students_df)
        st.success("Sample data loaded (23 credits, splitting enabled)")
    else:
        # Upload logic similar to original
        st.warning("Upload files for custom data")
        return
    
    if st.button("Generate"):
        progress_bar = st.progress(0)
        status = st.empty()
        
        def callback(gen, total, fit, viol):
            progress_bar.progress((gen + 1) / total)
            status.text(f"Gen {gen+1}/{total}, Fitness: {fit:.3f}, Violations: {viol}")
        
        best, history = generator.evolve(callback)
        st.session_state['best'] = best
        st.session_state['gen'] = generator
        
        st.success("Generated!")
        display_enhanced_timetable(best, generator)

if __name__ == "__main__":
    main()