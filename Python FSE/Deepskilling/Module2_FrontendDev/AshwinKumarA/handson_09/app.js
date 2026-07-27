import { courses } from "./data.js";

/*
==========================================================
HANDS-ON 4

Fetch vs Axios

1. Fetch is built into modern browsers. Axios is an external library.
2. Fetch requires response.ok checking. Axios throws automatically for non-2xx responses.
3. Fetch requires response.json(). Axios automatically parses JSON.
==========================================================

HANDS-ON 09 - TASK 3 FEATURE SUPPORT

Feature checked:
CSS Grid using display: grid.

Browser-support research:
The exact support findings must be recorded after checking caniuse.com.

Feature detection:
CSS.supports("display", "grid") checks the feature rather than
guessing from the browser name.

Fallback:
styles.css includes an @supports not (display: grid) Flexbox layout.
*/

courses.forEach(({ name, credits }) => {
    console.log(`${name} has ${credits} credits.`);
});

const formattedCourses = courses.map(
    ({ code, name, credits }) =>
        `${code} — ${name} (${credits} credits)`
);

console.log(formattedCourses);

const fourCreditCourses = courses.filter(
    ({ credits }) => credits >= 4
);

console.log(fourCreditCourses);

const totalCredits = courses.reduce(
    (total, { credits }) => total + credits,
    0
);

console.log(`Total Credits: ${totalCredits}`);

// DOM References

const courseGrid = document.querySelector(".course-grid");
const totalCreditsElement = document.querySelector("#total-credits");
const searchInput = document.querySelector("#search-courses");
const sortButton = document.querySelector("#sort-credits");
const selectedCourse = document.querySelector("#selected-course");
const exploreButton = document.querySelector("#explore-courses");
const courseLoading = document.querySelector("#course-loading");
const menuButton = document.querySelector("#menu-button");
const mainNavigation = document.querySelector("#main-navigation");

const notificationLoading = document.querySelector(
    "#notification-loading"
);

const notificationList = document.querySelector(
    "#notification-list"
);

const notificationError = document.querySelector(
    "#notification-error"
);

let displayedCourses = [...courses];

const courseDescriptions = {
    HTML101:
        "Learn the basic structure and semantic elements of HTML5.",

    CSS102:
        "Learn selectors, colours, spacing and the CSS box model.",

    JS103:
        "Learn variables, functions and JavaScript concepts.",

    RWD104:
        "Responsive layouts using Flexbox and Grid.",

    FDT105:
        "Frontend development tools and DevTools."
};

// Feature Detection

if (
    typeof CSS !== "undefined" &&
    CSS.supports("display", "grid")
) {
    console.log("CSS Grid is supported.");
} else {
    console.log(
        "CSS Grid is not supported. Flexbox fallback is active."
    );
}

// Course Rendering

function renderCourses(courseList) {
    courseGrid.innerHTML = "";

    courseList.forEach((course) => {
        const card = document.createElement("article");

        card.className = "course-card";
        card.dataset.courseId = course.id;
        card.tabIndex = 0;

        card.setAttribute(
            "aria-label",
            `${course.name}, ${course.code}, ` +
            `${course.credits} credits, grade ${course.grade}`
        );

        card.innerHTML = `
            <h3>${course.name}</h3>

            <p class="course-code">
                ${course.code}
            </p>

            <p class="course-description">
                ${courseDescriptions[course.code]}
            </p>

            <p class="course-grade">
                Grade: ${course.grade}
            </p>

            <span>
                ${course.credits} Credits
            </span>
        `;

        card.addEventListener(
            "keydown",
            (event) => {
                if (event.key === "Enter") {
                    event.preventDefault();
                    card.click();
                }
            }
        );

        courseGrid.appendChild(card);
    });

    if (courseList.length === 0) {
        const noCoursesMessage = document.createElement("p");

        noCoursesMessage.className = "no-courses";
        noCoursesMessage.textContent = "No courses found.";

        courseGrid.appendChild(noCoursesMessage);
    }
}

function updateCredits() {
    totalCreditsElement.textContent =
        `Total Credits Enrolled: ${totalCredits}`;
}

// Simulated Course Loading

function fetchAllCourses() {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(courses);
        }, 1000);
    });
}

async function loadCourses() {
    courseLoading.textContent = "Loading courses...";

    const result = await fetchAllCourses();

    displayedCourses = [...result];

    renderCourses(displayedCourses);
    updateCredits();

    courseLoading.textContent = "";
}

loadCourses();

// Fetch Promise Example

function fetchUser(id) {
    return fetch(
        `https://jsonplaceholder.typicode.com/users/${id}`
    )
        .then((response) => response.json())
        .then((user) => {
            console.log("Promise User:", user.name);

            return user;
        });
}

fetchUser(1);

// Async/Await Example

async function fetchUserAsync(id) {
    try {
        const response = await fetch(
            `https://jsonplaceholder.typicode.com/users/${id}`
        );

        const user = await response.json();

        console.log("Async User:", user.name);

        return user;
    } catch (error) {
        console.error(error);

        return null;
    }
}

fetchUserAsync(1);

// Promise.all Example

Promise.all([
    fetchUserAsync(1),
    fetchUserAsync(2)
]).then((users) => {
    console.log("Promise.all Result");

    users
        .filter((user) => user !== null)
        .forEach((user) => {
            console.log(user.name);
        });
});

// Reusable Fetch Function

async function apiFetch(url) {
    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(
            `Request failed: ${response.status}`
        );
    }

    return response.json();
}

// Notification Rendering

function renderNotifications(posts) {
    notificationList.innerHTML = "";

    posts.slice(0, 5).forEach((post) => {
        const article = document.createElement("article");

        article.className = "notification-card";

        article.innerHTML = `
            <h3>${post.title}</h3>
            <p>${post.body}</p>
        `;

        notificationList.appendChild(article);
    });
}

async function loadNotifications() {
    notificationLoading.textContent =
        "Loading notifications...";

    notificationError.innerHTML = "";

    try {
        const posts = await apiFetch(
            "https://jsonplaceholder.typicode.com/posts"
        );

        renderNotifications(posts);
    } catch (error) {
        const errorBox = document.createElement("div");

        errorBox.className = "error-box";
        errorBox.textContent = error.message;

        notificationError.appendChild(errorBox);
    } finally {
        notificationLoading.textContent = "";
    }
}

loadNotifications();

// Simulated Error and Retry

async function showErrorDemo() {
    try {
        await apiFetch(
            "https://jsonplaceholder.typicode.com/nonexistent"
        );
    } catch {
        notificationError.innerHTML = "";

        const errorBox = document.createElement("div");

        errorBox.className = "error-box";

        const errorMessage = document.createElement("p");

        errorMessage.textContent =
            "Unable to load notifications.";

        const retryButton = document.createElement("button");

        retryButton.id = "retry-button";
        retryButton.className = "retry-button";
        retryButton.type = "button";
        retryButton.textContent = "Retry";

        retryButton.setAttribute(
            "aria-label",
            "Retry loading notifications"
        );

        errorBox.appendChild(errorMessage);
        errorBox.appendChild(retryButton);

        notificationError.appendChild(errorBox);
    }
}

showErrorDemo();

notificationError.addEventListener(
    "click",
    (event) => {
        const retryButton = event.target.closest(
            "#retry-button"
        );

        if (!retryButton) {
            return;
        }

        loadNotifications();
    }
);

// Mobile Menu

if (menuButton && mainNavigation) {
    menuButton.addEventListener(
        "click",
        () => {
            const isExpanded =
                menuButton.getAttribute("aria-expanded") ===
                "true";

            const newState = !isExpanded;

            menuButton.setAttribute(
                "aria-expanded",
                newState.toString()
            );

            menuButton.setAttribute(
                "aria-label",
                newState
                    ? "Close main navigation"
                    : "Open main navigation"
            );

            mainNavigation.classList.toggle(
                "nav-open",
                newState
            );
        }
    );
}

// Main Application Events

exploreButton.addEventListener(
    "click",
    () => {
        document
            .querySelector("#courses")
            .scrollIntoView({
                behavior: "smooth"
            });
    }
);

searchInput.addEventListener(
    "input",
    (event) => {
        const term = event.target.value
            .trim()
            .toLowerCase();

        displayedCourses = courses.filter(
            ({ name }) =>
                name
                    .toLowerCase()
                    .includes(term)
        );

        renderCourses(displayedCourses);

        const noun =
            displayedCourses.length === 1
                ? "course"
                : "courses";

        selectedCourse.textContent =
            `${displayedCourses.length} ${noun} found.`;
    }
);

sortButton.addEventListener(
    "click",
    () => {
        displayedCourses = [...displayedCourses].sort(
            (firstCourse, secondCourse) =>
                secondCourse.credits -
                firstCourse.credits
        );

        renderCourses(displayedCourses);

        selectedCourse.textContent =
            "Courses sorted by credits.";
    }
);

courseGrid.addEventListener(
    "click",
    (event) => {
        const card = event.target.closest(
            ".course-card"
        );

        if (!card) {
            return;
        }

        const id = Number(card.dataset.courseId);

        const course = courses.find(
            (currentCourse) =>
                currentCourse.id === id
        );

        if (!course) {
            return;
        }

        selectedCourse.textContent =
            `Selected Course: ${course.name} | ` +
            `Grade: ${course.grade}`;
    }
);

// Axios

axios.interceptors.request.use((config) => {
    console.log(
        `API call started: ${config.url}`
    );

    return config;
});

async function axiosPosts() {
    try {
        const response = await axios.get(
            "https://jsonplaceholder.typicode.com/posts",
            {
                params: {
                    userId: 1
                }
            }
        );

        console.log(
            "Axios Posts",
            response.data
        );
    } catch (error) {
        console.error(
            "Axios request failed:",
            error.message
        );
    }
}

axiosPosts();