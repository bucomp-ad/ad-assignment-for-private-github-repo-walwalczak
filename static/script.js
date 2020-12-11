window.addEventListener('load', function () {
  
  // [START gae_python38_auth_signout]
  document.getElementById('sign-out').onclick = function () {
    window.location.href='/';
    firebase.auth().signOut();
  };
  // [END gae_python38_auth_signout]

  // [START gae_python38_auth_UIconfig_variable]
  // FirebaseUI config.
  var uiConfig = {
    signInSuccessUrl: '/',
    signInOptions: [
      // Remove any lines corresponding to providers you did not check in
      // the Firebase console.
      firebase.auth.GoogleAuthProvider.PROVIDER_ID,
      firebase.auth.EmailAuthProvider.PROVIDER_ID,
    ],
    // Terms of service url.
    tosUrl: '<your-tos-url>'
  };
  // [END gae_python38_auth_UIconfig_variable]

  // [START gae_python38_auth_request]
  firebase.auth().onAuthStateChanged(function (user) {
    if (user) {

      var displayName = user.displayName;
      var email = user.email;
      var emailVerified = user.emailVerified;
      var photoURL = user.photoURL;
      var uid = user.uid;
      var phoneNumber = user.phoneNumber;
      var providerData = user.providerData;
      let itemCards = document.getElementById('item-cards')

      // User is signed in, so display the "sign out" button and login info.
      document.getElementById('sign-out').hidden = false;

      if (itemCards) {
        itemCards.hidden = false;
      }

      console.log(`Signed in as ${user.displayName} (${user.email})`);
      $('#login-info').html(`Signed in as ${displayName} (${email})`)
    
      user.getIdToken().then(function (token) {

        document.cookie = "token=" + token;
      });
    } else {
      // User is signed out.
      // Initialize the FirebaseUI Widget using Firebase.

      var ui = new firebaseui.auth.AuthUI(firebase.auth());
      // Show the Firebase login button.
      ui.start('#firebaseui-auth-container', uiConfig);
      // Update the login state indicators.
      document.getElementById('sign-out').hidden = true;
      document.getElementById('login-info').hidden = true;
      if (document.getElementById('item-cards')){
        document.getElementById('item-cards').hidden = true;
      }
      // Clear the token cookie.
      document.cookie = "token=";
    }
  }, function (error) {
    console.log(error);
    alert('Unable to log in: ' + error)
  });
  // [END gae_python38_auth_request]
});

