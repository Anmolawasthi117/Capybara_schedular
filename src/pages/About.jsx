function About() {
  return (
    <section className="min-h-screen bg-white flex flex-col items-center justify-center px-6 text-center">
      <h1 className="text-4xl md:text-5xl font-semibold text-green-600 mb-4">
        About This Project
      </h1>
      <p className="text-base md:text-lg text-gray-700 max-w-2xl">
        This frontend template is crafted for speed and simplicity. It uses Vite for blazing fast builds,
        TailwindCSS for modern utility-first styling, and React Router DOM for page routing. It’s meant to be
        a clean slate to kickstart any kind of single-page or full-stack project.
      </p>
    </section>
  );
}

export default About;
