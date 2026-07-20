import { courses } from "./data.js";

/*
==========================================================
HANDS-ON 4

Fetch vs Axios

1. Fetch is built into modern browsers. Axios is an external library.
2. Fetch requires response.ok checking. Axios throws automatically for non-2xx responses.
3. Fetch requires response.json(). Axios automatically parses JSON.
==========================================================
*/

// ------------------------------
// Hands-On 3 Console Exercises
// ------------------------------

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

// ------------------------------
// DOM
// ------------------------------

const courseGrid = document.querySelector(".course-grid");
const totalCreditsElement = document.querySelector("#total-credits");
const searchInput = document.querySelector("#search-courses");
const sortButton = document.querySelector("#sort-credits");
const selectedCourse = document.querySelector("#selected-course");
const exploreButton = document.querySelector("#explore-courses");

const courseLoading = document.querySelector("#course-loading");

const notificationLoading = document.querySelector("#notification-loading");
const notificationList = document.querySelector("#notification-list");
const notificationError = document.querySelector("#notification-error");

let displayedCourses = [...courses];

const courseDescriptions = {
    HTML101: "Learn the basic structure and semantic elements of HTML5.",
    CSS102: "Learn selectors, colours, spacing and the CSS box model.",
    JS103: "Learn variables, functions and JavaScript concepts.",
    RWD104: "Responsive layouts using Flexbox and Grid.",
    FDT105: "Frontend development tools and DevTools."
};

// ------------------------------
// Course Rendering
// ------------------------------

function renderCourses(courseList) {

    courseGrid.innerHTML = "";

    courseList.forEach((course) => {

        const card = document.createElement("article");

        card.className = "course-card";
        card.dataset.courseId = course.id;

        card.innerHTML = `
            <h3>${course.name}</h3>
            <p class="course-code">${course.code}</p>
            <p class="course-description">${courseDescriptions[course.code]}</p>
            <p class="course-grade">Grade : ${course.grade}</p>
            <span>${course.credits} Credits</span>
        `;

        courseGrid.appendChild(card);

    });

    if (courseList.length === 0) {

        const p = document.createElement("p");

        p.className = "no-courses";
        p.textContent = "No courses found.";

        courseGrid.appendChild(p);

    }

}

function updateCredits() {

    totalCreditsElement.textContent =
        `Total Credits Enrolled : ${totalCredits}`;

}

// ------------------------------
// Step 47
// Simulated delay
// ------------------------------

function fetchAllCourses() {

    return new Promise((resolve) => {

        setTimeout(() => {

            resolve(courses);

        }, 1000);

    });

}

// ------------------------------
// Step 48
// ------------------------------

async function loadCourses() {

    courseLoading.textContent = "Loading courses...";

    const result = await fetchAllCourses();

    displayedCourses = [...result];

    renderCourses(displayedCourses);

    updateCredits();

    courseLoading.textContent = "";

}

loadCourses();

// ------------------------------
// Step 45
// Promise then()
// ------------------------------

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

// ------------------------------
// Step 46
// async await
// ------------------------------

async function fetchUserAsync(id) {

    try {

        const response =
            await fetch(
                `https://jsonplaceholder.typicode.com/users/${id}`
            );

        const user = await response.json();

        console.log("Async User:", user.name);

        return user;

    }
    catch (error) {

        console.error(error);

    }

}

fetchUserAsync(1);

// ------------------------------
// Step 49
// Promise.all()
// ------------------------------

Promise.all([
    fetchUserAsync(1),
    fetchUserAsync(2)
]).then((users) => {

    console.log("Promise.all Result");

    users.forEach((user) => {

        console.log(user.name);

    });

});

// ------------------------------
// Step 50
// Reusable Fetch API
// ------------------------------

async function apiFetch(url) {

    const response = await fetch(url);

    if (!response.ok) {

        throw new Error(
            `Request failed : ${response.status}`
        );

    }

    return response.json();

}

// ------------------------------
// Notifications
// ------------------------------

function renderNotifications(posts) {

    notificationList.innerHTML = "";

    posts.slice(0, 5).forEach((post) => {

        const article =
            document.createElement("article");

        article.className =
            "notification-card";

        article.innerHTML = `
            <h3>${post.title}</h3>
            <p>${post.body}</p>
        `;

        notificationList.appendChild(article);

    });

}

// ------------------------------
// Step 51
// ------------------------------

async function loadNotifications() {

    notificationLoading.textContent =
        "Loading notifications...";

    notificationError.innerHTML = "";

    try {

        const posts =
            await apiFetch(
                "https://jsonplaceholder.typicode.com/posts"
            );

        renderNotifications(posts);

    }

    catch (error) {

        notificationError.innerHTML = `
            <div class="error-box">
                ${error.message}
            </div>
        `;

    }
    finally {

        notificationLoading.textContent = "";

    }

}

loadNotifications();

// ------------------------------
// Step 53
// Simulated Error
// ------------------------------

async function showErrorDemo() {

    try {

        await apiFetch(
            "https://jsonplaceholder.typicode.com/nonexistent"
        );

    }
    catch {

        notificationError.innerHTML = `
            <div class="error-box">
                Unable to load notifications.

                <br><br>

                <button
                    id="retry-button"
                    class="retry-button">

                    Retry

                </button>
            </div>
        `;

    }

}

showErrorDemo();

// ------------------------------
// Step 54
// Retry
// ------------------------------

notificationError.addEventListener(
    "click",
    (event) => {

        if (event.target.id !== "retry-button") {

            return;

        }

        loadNotifications();

    }
);

// ------------------------------
// Hands-On 3 Events
// ------------------------------

exploreButton.addEventListener(
    "click",
    () => {

        document.querySelector("#courses")
            .scrollIntoView({
                behavior: "smooth"
            });

    }
);

searchInput.addEventListener(
    "input",
    (event) => {

        const term =
            event.target.value
                .trim()
                .toLowerCase();

        displayedCourses =
            courses.filter(
                ({ name }) =>
                    name.toLowerCase()
                        .includes(term)
            );

        renderCourses(displayedCourses);

        selectedCourse.textContent =
            `${displayedCourses.length} course(s) found.`;

    }
);

sortButton.addEventListener(
    "click",
    () => {

        displayedCourses =
            [...displayedCourses].sort(
                (a, b) =>
                    b.credits - a.credits
            );

        renderCourses(displayedCourses);

        selectedCourse.textContent =
            "Courses sorted by credits.";

    }
);

courseGrid.addEventListener(
    "click",
    (event) => {

        const card =
            event.target.closest(".course-card");

        if (!card) {

            return;

        }

        const id =
            Number(card.dataset.courseId);

        const course =
            courses.find(
                (c) => c.id === id
            );

        if (!course) {

            return;

        }

        selectedCourse.textContent =
            `Selected Course : ${course.name} | Grade : ${course.grade}`;

    }
);

// ------------------------------
// Step 55–58
// Axios
// ------------------------------

axios.interceptors.request.use((config) => {

    console.log(
        `API call started: ${config.url}`
    );

    return config;

});

async function axiosPosts() {

    const response =
        await axios.get(
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

}

axiosPosts();