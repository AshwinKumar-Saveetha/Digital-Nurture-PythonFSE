function CourseCard({
  id,
  name,
  code,
  credits,
  grade,
  onEnroll,
  onViewDetails
}) {
  return (
    <div className="course-card">
      <h3>{name}</h3>

      <p>
        <strong>Code:</strong> {code}
      </p>

      <p>
        <strong>Credits:</strong> {credits}
      </p>

      <p>
        <strong>Grade:</strong> {grade}
      </p>

      <button
        type="button"
        className="details-btn"
        onClick={() => onViewDetails(id)}
      >
        View Details
      </button>

      <button
        type="button"
        className="enroll-btn"
        onClick={onEnroll}
      >
        Enroll
      </button>
    </div>
  );
}

export default CourseCard;