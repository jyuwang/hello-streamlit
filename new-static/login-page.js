const loginForm = document.getElementById("login-form");
const loginButton = document.getElementById("login-form-submit");
const loginErrorMsg = document.getElementById("login-error-msg");
let intervalID = 0;
let stopCheck = false;

// When the login button is clicked, the following code is executed
loginButton.addEventListener("click", (e) => {
  // Prevent the default submission of the form
  e.preventDefault();
  // Get the values input by the user in the form fields
  const email = loginForm.email.value;
  sendLoginRequest(email);
});

function sendLoginRequest(email) {
  // Define the URL
  const url = "http://127.0.0.1:5000/login";

  // Define the request body
  const requestBody = {
    email: email,
  };

  // Define request options
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(requestBody),
  };

  // Send the POST request
  fetch(url, options)
    .then((response) => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error("Failed to send login request");
      }
    })
    .then((data) => {
      console.log(data); // Handle the response data here
      // every 2 seconds, poll last endpoint
      // Call the API every 2 seconds
      //   intervalID = setInterval(checkValid(email), 2000);
      //checkValid(email);

      //   `GET: /check_authentication?email=nigelchen2014@gmail.com`;
    })
    .catch((error) => {
      console.error("Error:", error);
    });

  pollEndpoint(email);
}

function checkValid(email) {
  fetch("/check_authentication?email=" + email)
    .then((response) => response.json())
    .then((data) => {
      // Check if response is true or false
      if (data.authenticated === true) {
        console.log("User is authenticated");
        alert("You have successfully logged in.");
        stopCheck = true;
      } else if (data === false) {
        console.log("User is not authenticated");
        loginErrorMsg.style.opacity = 1;
      } else {
        console.log("Invalid response");
        stopCheck = true;
      }
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });

  if (stopCheck) {
    return;
  } else {
    console.log("calling checkValid again in 5 seconds");
  }
}

function pollEndpoint(email) {
  setInterval(() => {
    checkValid(email);
  }, 2000);
}
