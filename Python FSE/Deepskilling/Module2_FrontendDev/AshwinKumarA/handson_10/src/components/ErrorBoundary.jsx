import { Component } from "react";

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);

    this.state = {
      hasError: false,
      errorMessage: "",
    };
  }

  static getDerivedStateFromError(error) {
    return {
      hasError: true,
      errorMessage:
        error.message ||
        "An unexpected application error occurred.",
    };
  }

  componentDidCatch(error, errorInfo) {
    console.error(
      "Application Error:",
      error,
      errorInfo,
    );
  }

  handleReload = () => {
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <main className="container">
          <section
            className="api-error-message"
            role="alert"
          >
            <h1>Something Went Wrong</h1>

            <p>
              The Student Portal encountered an
              unexpected error.
            </p>

            <p>{this.state.errorMessage}</p>

            <button
              type="button"
              className="primary-button"
              onClick={this.handleReload}
            >
              Reload Application
            </button>
          </section>
        </main>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;