function Header({ siteName, enrolledCount }) {
  return (
    <header className="header">
      <h1>{siteName}</h1>

      <p className="enrolled-count">
        Enrolled Courses : {enrolledCount}
      </p>
    </header>
  );
}

export default Header;