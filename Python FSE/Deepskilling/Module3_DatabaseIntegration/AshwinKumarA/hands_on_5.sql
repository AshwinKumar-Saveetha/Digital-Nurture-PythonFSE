-- ============================================
-- HANDS-ON 5 : MongoDB CRUD & Aggregation
-- ============================================

use college_nosql

-- Verify document count
db.feedback.countDocuments()

-- READ Operations
db.feedback.find({ rating: 5 })

db.feedback.find({
    course_code: "CS101",
    tags: "challenging"
})

db.feedback.find(
    {},
    {
        student_id: 1,
        course_code: 1,
        rating: 1,
        _id: 0
    }
)

-- UPDATE Operations
db.feedback.updateMany(
    { rating: { $lt: 3 } },
    { $set: { needs_review: true } }
)

db.feedback.updateMany(
    { needs_review: true },
    { $push: { tags: "reviewed" } }
)

-- DELETE Operation
db.feedback.deleteMany(
    { semester: "2021-EVEN" }
)

-- Aggregation Pipeline
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

-- Tag Frequency
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

-- Index
db.feedback.createIndex({ course_code: 1 })

-- Verify Index Usage
db.feedback.find({
    course_code: "CS101"
}).explain("executionStats")

-- Expected:
-- Winning plan should show IXSCAN instead of COLLSCAN.
