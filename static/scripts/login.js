function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
  
    // Basic validation
    if (!username || !password) {
      alert("Please enter both username and password.");
      return;
    }
  
    // Send login request to the server
    fetch("/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          window.location.href = "/"; // Redirect to home page
        } else {
          alert("Invalid username or password.");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("An error occurred. Please try again.");
      });
  }