# How to Contribute: Web Designers

Welcome to **Resume_Builder_AIHawk**! As a web designer, you have the exciting opportunity to contribute your custom CSS styles to our project. This not only allows you to showcase your design skills but also helps improve the resume templates for everyone. Here's a step-by-step guide on how to add your styles and contribute to the project.
Once your styles are merged, they will also be added to the principal repository at [feder-cr/linkedIn_auto_jobs_applier_with_AI](https://github.com/feder-cr/linkedIn_auto_jobs_applier_with_AI), which has around 11k stars. This offers a significant opportunity for exposure and publicity for your work.

Thank you for contributing and helping to make our resume templates even better!

## Create and Add Your Custom CSS

### 1. **Design Your Custom CSS**

Create a new CSS file to introduce your unique styling for the resume templates. Follow the HTML structure outlined below to ensure compatibility:

### **HTML Structure to Follow:**

```html
<body>
    <header>
        <h1>[Name and Surname]</h1>
        <div class="contact-info">
            <p class="fas fa-map-marker-alt">
                <span>[Your City, Your Country]</span>
            </p>
            <p class="fas fa-phone">
                <span>[Your Prefix Phone number]</span>
            </p>
            <p class="fas fa-envelope">
                <span>[Your Email]</span>
            </p>
            <p class="fab fa-linkedin">
                <a href="[Link LinkedIn account]">LinkedIn</a>
            </p>
            <p class="fab fa-github">
                <a href="[Link GitHub account]">GitHub</a>
            </p>
        </div>
    </header>

    <main>
        <section id="education">
            <h2>Education</h2>
            <div class="entry">
              <div class="entry-header">
                  <span class="entry-name">[University Name]</span>
                  <span class="entry-location">[Location] </span>
              </div>
              <div class="entry-details">
                  <span class="entry-title">[Degree] in [Field of Study] | Grade: [Your Grade]</span>
                  <span class="entry-year">[Start Year] – [End Year]  </span>
              </div>
              <ul class="compact-list">
                  <li>[Course Name] → Grade: [Grade]</li>
                  <li>[Course Name] → Grade: [Grade]</li>
                  <li>[Course Name] → Grade: [Grade]</li>
                  <li>[Course Name] → Grade: [Grade]</li>
                  <li>[Course Name] → Grade: [Grade]</li>
              </ul>
            </div>
        </section>
    
        <section id="work-experience">
            <h2>Work Experience</h2>
            <div class="entry">
                <div class="entry-header">
                    <span class="entry-name">[Company Name]</span>
                    <span class="entry-location"> — [Location]</span>
                </div>
                <div class="entry-details">
                    <span class="entry-title">[Your Job Title]</span>
                    <span class="entry-year">[Start Date] – [End Date]</span>
                </div>
                <ul class="compact-list">
                    <li>[Describe your responsibilities and achievements in this role]</li>
                    <li>[Describe any key projects or technologies you worked with]</li>
                    <li>[Mention any notable accomplishments or results]</li>
                </ul>
            </div>
            <div class="entry">
                <div class="entry-header">
                    <span class="entry-name">[Company Name]</span>
                    <span class="entry-location"> — [Location]</span>
                </div>
                <div class="entry-details">
                    <span class="entry-title">[Your Job Title]</span>
                    <span class="entry-year">[Start Date] – [End Date]</span>
                </div>
                <ul class="compact-list">
                    <li>[Describe your responsibilities and achievements in this role]</li>
                    <li>[Describe any key projects or technologies you worked with]</li>
                    <li>[Mention any notable accomplishments or results]</li>
                </ul>
            </div>
            <div class="entry">
                <div class="entry-header">
                    <span class="entry-name">[Company Name]</span>
                    <span class="entry-location"> — [Location]</span>
                </div>
                <div class="entry-details">
                    <span class="entry-title">[Your Job Title]</span>
                    <span class="entry-year">[Start Date] – [End Date]</span>
                </div>
                <ul class="compact-list">
                    <li>[Describe your responsibilities and achievements in this role]</li>
                    <li>[Describe any key projects or technologies you worked with]</li>
                    <li>[Mention any notable accomplishments or results]</li>
                </ul>
            </div>
        </section>
    
        <section id="side-projects">
            <h2>Side Projects</h2>
            <div class="entry">
                <div class="entry-header">
                    <span class="entry-name"><i class="fab fa-github"></i> <a href="[Github Repo or Link]">[Project Name]</a></span>
                </div>
                <ul class="compact-list">
                    <li>[Describe any notable recognition or reception]</li>
                    <li>[Describe any notable recognition or reception]</li>
                </ul>
            </div>
            <div class="entry">
                <div class="entry-header">
                    <span class="entry-name"><i class="fab fa-github"></i> <a href="[Github Repo or Link]">[Project Name]</a></span>
                </div>
                <ul class="compact-list">
                    <li>[Describe any notable recognition or reception]</li>
                    <li>[Describe any notable recognition or reception]</li>
                </ul>
            </div>
            <div class="entry">
                <div class="entry-header">
                    <span class="entry-name"><i class="fab fa-github"></i> <a href="[Github Repo or Link]">[Project Name]</a></span>
                </div>
                <ul class="compact-list">
                    <li>[Describe any notable recognition or reception]</li>
                    <li>[Describe any notable recognition or reception]</li>
                </ul>
            </div>
        </section>
    
        <section id="achievements">
            <h2>Achievements</h2>
            <ul class="compact-list">
                <li><strong>[Award or Recognition or Scholarship or Honor]:</strong> [Describe]</li>
                <li><strong>[Award or Recognition or Scholarship or Honor]:</strong> [Describe]</li>
                <li><strong>[Award or Recognition or Scholarship or Honor]:</strong> [Describe]</li>
            </ul>
        </section>

        <section id="certifications">
            <h2>Certifications</h2>
            <ul class="compact-list">
              <li><strong>[Certification Name]:</strong> [Describe]</li>
              <li><strong>[Certification Name]:</strong> [Describe]</li>
            </ul>
        </section>
    
        <section id="skills-languages">
            <h2>Additional Skills</h2>
            <div class="two-column">
                <ul class="compact-list">
                    <li>[Specific Skill or Technology]</li>
                    <li>[Specific Skill or Technology]</li>
                    <li>[Specific Skill or Technology]</li>
                    <li>[Specific Skill or Technology]</li>
                    <li>[Specific Skill or Technology]</li>
                    <li>[Specific Skill or Technology]</li>
                </ul>
                <ul class="compact-list">
                    <li>[Specific Skill or Technology]</li>
                    <li>[Specific Skill or Technology]</li>
                    <li>[Specific Skill or Technology]</li>
                    <li>[Specific Skill or Technology]</li>
                    <li>[Specific Skill or Technology]</li>
                    <li><strong>Languages:</strong></li>
                </ul>
            </div>
        </section>
    </main>
</body>
```
## Contribute

1. **Fork the Repository**

   - Visit the [Resume_Builder_AIHawk GitHub repository](https://github.com/feder-cr/lib_resume_builder_AIHawk).
   - Click the **Fork** button at the top right of the page. This creates a copy of the repository under your GitHub account.

2. **Clone Your Fork**

   - Clone your forked repository to your local machine:

     ```bash
     git clone https://github.com/yourusername/lib_resume_builder_AIHawk.git
     cd lib_resume_builder_AIHawk
     ```

3. **Create a New Branch (Optional but Recommended)**

   - It’s a good practice to create a new branch for your changes:

     ```bash
     git checkout -b feature/custom-style
     ```

## Create and Add Your Custom CSS

4. **Add Your CSS File**

   - Navigate to the `resume_style` directory in your local copy:

     ```bash
     cd lib_resume_builder_AIHawk/resume_style
     ```

   - Create a new CSS file, for example, `custom-style.css`, and add your custom styles to this file.

5. **Test Your Styles**

   - Ensure that your CSS file works well with the sample resume data.
   - Check for visual consistency, responsiveness, and cross-browser compatibility.

## Submit Your Contribution

6. **Commit Your Changes**

   - Add and commit your changes:

     ```bash
     git add lib_resume_builder_AIHawk/resume_style/custom-style.css
     git commit -m "Add custom CSS styles"
     ```

7. **Push Your Changes**

   - Push your changes to your forked repository:

     ```bash
     git push origin feature/custom-style
     ```

8. **Create a Pull Request**

   - Go to your forked repository on GitHub.
   - Click on the **Compare & pull request** button.
   - Provide a description of your changes and how they enhance the project.
   - Click **Create pull request** to submit it for review.

---

## Need Assistance?

If you have any questions or need help with your contribution, please join our [Telegram community](https://t.me/AIhawkCommunity). We're here to support you with any issues or doubts!

Thank you for contributing to **Resume_Builder_AIHawk**! Your creative designs help improve our resume tool and benefit all users. 🚀
