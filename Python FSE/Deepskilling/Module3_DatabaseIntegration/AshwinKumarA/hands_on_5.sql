// ============================================================
// Digital Nurture 5.0 - Module 3: Database Integration
// HANDS-ON 5 [Intermediate]
// MongoDB - Document Modelling, CRUD & Aggregation
// Tool: mongosh (MongoDB Shell)
// NOTE: file kept with a .sql extension per the required project
// layout, but the content below is MongoDB Shell (JavaScript)
// syntax, not SQL - run it with `mongosh < hands_on_5.sql` or
// paste the commands into mongosh / MongoDB Compass.
// ============================================================

// --------------------------------------------------------------
// TASK 1: Create the Collection and Insert Documents
// --------------------------------------------------------------

// Step 60: switch to (and implicitly create) the college_nosql database
use college_nosql

// Step 61-63: create the feedback collection and insert at least
// 10 realistic documents. Ratings, tags and semesters are varied.
// At least 3 documents reference CS101 and 2 reference CS102.
// The last document intentionally omits "attachments" to show
// MongoDB's schema-less design.
db.feedback.insertMany([
    {
        student_id: 1,
        course_code: "CS101",
        semester: "2022-ODD",
        rating: 5,
        comments: "Excellent teaching. Would recommend.",
        tags: ["challenging", "well-structured", "good-examples"],
        submitted_at: ISODate("2022-11-30T10:15:00Z"),
        attachments: [{ filename: "notes.pdf", size_kb: 240 }]
    },
    {
        student_id: 2,
        course_code: "CS101",
        semester: "2022-ODD",
        rating: 4,
        comments: "Good pace, clear examples.",
        tags: ["well-structured", "good-examples"],
        submitted_at: ISODate("2022-11-30T11:00:00Z"),
        attachments: [{ filename: "summary.pdf", size_kb: 120 }]
    },
    {
        student_id: 5,
        course_code: "CS101",
        semester: "2022-ODD",
        rating: 2,
        comments: "Too fast-paced for beginners.",
        tags: ["challenging"],
        submitted_at: ISODate("2022-11-30T12:30:00Z"),
        attachments: [{ filename: "feedback.pdf", size_kb: 80 }]
    },
    {
        student_id: 1,
        course_code: "CS102",
        semester: "2022-ODD",
        rating: 5,
        comments: "Loved the database design module.",
        tags: ["well-structured", "practical"],
        submitted_at: ISODate("2022-12-01T09:00:00Z"),
        attachments: [{ filename: "er-diagram.pdf", size_kb: 300 }]
    },
    {
        student_id: 5,
        course_code: "CS102",
        semester: "2022-ODD",
        rating: 3,
        comments: "Average, needs more practicals.",
        tags: ["needs-improvement"],
        submitted_at: ISODate("2022-12-01T09:45:00Z"),
        attachments: [{ filename: "review.pdf", size_kb: 60 }]
    },
    {
        student_id: 3,
        course_code: "EC101",
        semester: "2021-EVEN",
        rating: 4,
        comments: "Solid fundamentals coverage.",
        tags: ["well-structured"],
        submitted_at: ISODate("2021-05-20T14:00:00Z"),
        attachments: [{ filename: "circuit-notes.pdf", size_kb: 150 }]
    },
    {
        student_id: 6,
        course_code: "EC101",
        semester: "2021-EVEN",
        rating: 1,
        comments: "Very confusing lectures.",
        tags: ["challenging", "needs-improvement"],
        submitted_at: ISODate("2021-05-21T10:00:00Z"),
        attachments: [{ filename: "complaint.pdf", size_kb: 40 }]
    },
    {
        student_id: 4,
        course_code: "ME101",
        semester: "2023-ODD",
        rating: 5,
        comments: "Great real-world examples.",
        tags: ["good-examples", "practical"],
        submitted_at: ISODate("2023-11-15T13:00:00Z"),
        attachments: [{ filename: "lab-report.pdf", size_kb: 200 }]
    },
    {
        student_id: 7,
        course_code: "ME101",
        semester: "2023-ODD",
        rating: 4,
        comments: "Enjoyed the lab sessions.",
        tags: ["practical"],
        submitted_at: ISODate("2023-11-16T13:30:00Z"),
        attachments: [{ filename: "lab-notes.pdf", size_kb: 90 }]
    },
    {
        student_id: 8,
        course_code: "CS101",
        semester: "2022-ODD",
        rating: 5,
        comments: "Best course this semester.",
        tags: ["well-structured", "challenging", "good-examples"],
        submitted_at: ISODate("2022-12-02T08:20:00Z")
        // attachments field intentionally omitted (Step 63)
    }
]);

// Step 64: verify the inserts
db.feedback.countDocuments()


// --------------------------------------------------------------
// TASK 2: CRUD Operations
// --------------------------------------------------------------

// Step 65: READ - all feedback with rating 5
db.feedback.find({ rating: 5 })

// Step 66: READ - CS101 feedback tagged "challenging"
db.feedback.find({
    course_code: "CS101",
    tags: "challenging"
})

// Step 67: READ - projection of student_id, course_code, rating only
db.feedback.find(
    {},
    {
        student_id: 1,
        course_code: 1,
        rating: 1,
        _id: 0
    }
)

// Step 68: UPDATE - flag all low ratings ( < 3 ) for review
db.feedback.updateMany(
    { rating: { $lt: 3 } },
    { $set: { needs_review: true } }
)

// Step 69: UPDATE - push a "reviewed" tag onto every flagged document
db.feedback.updateMany(
    { needs_review: true },
    { $push: { tags: "reviewed" } }
)

// Step 70: DELETE - remove feedback from the 2021-EVEN semester
db.feedback.deleteMany(
    { semester: "2021-EVEN" }
)


// --------------------------------------------------------------
// TASK 3: Aggregation Pipeline
// --------------------------------------------------------------

// Step 71-72: average rating and feedback count per course for
// 2022-ODD, renamed/rounded via $project, sorted best-first
db.feedback.aggregate([
    { $match: { semester: "2022-ODD" } },
    {
        $group: {
            _id: "$course_code",
            avg_rating: { $avg: "$rating" },
            total_feedback: { $sum: 1 }
        }
    },
    {
        $project: {
            _id: 0,
            course_code: "$_id",
            average_rating: { $round: ["$avg_rating", 1] },
            total_feedback: 1
        }
    },
    { $sort: { average_rating: -1 } }
])

// Step 73: tag frequency leaderboard
db.feedback.aggregate([
    { $unwind: "$tags" },
    {
        $group: {
            _id: "$tags",
            count: { $sum: 1 }
        }
    },
    { $sort: { count: -1 } }
])

// Step 74: index on course_code, then verify it is actually used
db.feedback.createIndex({ course_code: 1 })

db.feedback.find({
    course_code: "CS101"
}).explain("executionStats")

// Expected: the winning plan should show IXSCAN instead of COLLSCAN.
