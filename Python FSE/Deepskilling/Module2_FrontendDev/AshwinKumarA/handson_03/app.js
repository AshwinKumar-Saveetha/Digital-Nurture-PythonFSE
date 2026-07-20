import { courses } from "./data.js";

/*
    HANDS-ON 3
    JavaScript ES6+ and DOM Manipulation
*/

// Step 30: Use destructuring to extract name and credits.
courses.forEach((course) => {
    const { name, credits } = course;
    console.log(`${name} has ${credits} credits.`);
});

// Step 31: Use map() to create formatted course strings.
const formattedCourses = courses.map(
    ({ code, name, credits }) =>
        `${code} — ${name} (${credits} credits)`
);

console.log("Formatted course strings:");
console.log(formattedCourses);

// Step 32: Use filter() to find courses with credits greater than or equal to 4.
const fourCreditCourses = courses.filter(
    ({ credits }) => credits >= 4
);

console.log("Courses with credits greater than or equal to 4:");
console.log(fourCreditCourses);
console.log(`Number of courses with at least 4 credits: ${fourCreditCourses.length}`);

// Step 33: Use reduce() to calculate total credits.
const totalCredits = courses.reduce(
    (total, { credits }) => total + credits,
    0
);

console.log(`Total credits enrolled: ${totalCredits}`);

// Step 36: Select required DOM elements.
const courseGrid = document.querySelector(".course-grid");
const totalCreditsElement = document.querySelector("#total-credits");
const searchInput = document.querySelector("#search-courses");
const sortButton = document.querySelector("#sort-credits");
const selectedCourseElement = document.querySelector("#selected-course");
const exploreCoursesButton = document.querySelector("#explore-courses");

// Store the currently displayed course list.
let displayedCourses = [...courses];

// Course descriptions preserved from Hands-On 2.
const courseDescriptions = {
    HTML101: "Learn the basic structure and semantic elements of HTML5.",
    CSS102: "Learn selectors, colours, spacing and the CSS box model.",
    JS103: "Learn variables, functions and basic JavaScript concepts.",
    RWD104: "Learn how to create layouts for mobile, tablet and desktop.",
    FDT105: "Learn how to use browser DevTools and frontend development tools."
};

// Steps 34, 37 and 38:
// Arrow function, template literals, createElement() and appendChild().
const renderCourses = (courseList) => {
    // Clear existing cards before every re-render.
    courseGrid.innerHTML = "";

    courseList.forEach((course) => {
        const { id, name, code, credits, grade } = course;

        const courseCard = document.createElement("article");

        courseCard.className = "course-card";
        courseCard.dataset.courseId = id;

        courseCard.innerHTML = `
            <h3>${name}</h3>
            <p class="course-code">${code}</p>
            <p class="course-description">
                ${courseDescriptions[code]}
            </p>
            <p class="course-grade">Grade: ${grade}</p>
            <span>${credits} Credits</span>
        `;

        courseGrid.appendChild(courseCard);
    });

    if (courseList.length === 0) {
        const noCoursesMessage = document.createElement("p");

        noCoursesMessage.className = "no-courses";
        noCoursesMessage.textContent = "No courses found.";

        courseGrid.appendChild(noCoursesMessage);
    }
};

// Step 39: Display total credits dynamically using textContent.
const updateTotalCredits = () => {
    totalCreditsElement.textContent =
        `Total Credits Enrolled: ${totalCredits}`;
};

// Render the initial five courses.
renderCourses(displayedCourses);
updateTotalCredits();

// Explore Courses button scrolls to the existing courses section.
exploreCoursesButton.addEventListener("click", () => {
    document.querySelector("#courses").scrollIntoView({
        behavior: "smooth"
    });

    searchInput.focus();
});

// Steps 40 and 41:
// Filter by course name on every input event.
searchInput.addEventListener("input", (event) => {
    const searchTerm = event.target.value.trim().toLowerCase();

    displayedCourses = courses.filter(({ name }) =>
        name.toLowerCase().includes(searchTerm)
    );

    renderCourses(displayedCourses);

    selectedCourseElement.textContent =
        `${displayedCourses.length} course(s) found.`;
});

// Step 42:
// Sort the currently visible courses by credits descending.
sortButton.addEventListener("click", () => {
    displayedCourses = [...displayedCourses].sort(
        (firstCourse, secondCourse) =>
            secondCourse.credits - firstCourse.credits
    );

    renderCourses(displayedCourses);

    selectedCourseElement.textContent =
        "Courses sorted by credits from highest to lowest.";
});

// Steps 43 and 44:
// A single delegated listener handles all dynamically created cards.
courseGrid.addEventListener("click", (event) => {
    const clickedCard = event.target.closest(".course-card");

    if (!clickedCard || !courseGrid.contains(clickedCard)) {
        return;
    }

    const selectedCourseId = Number(clickedCard.dataset.courseId);

    const selectedCourse = courses.find(
        ({ id }) => id === selectedCourseId
    );

    if (!selectedCourse) {
        return;
    }

    const { name, grade } = selectedCourse;

    selectedCourseElement.textContent =
        `Selected Course: ${name} | Grade: ${grade}`;
});