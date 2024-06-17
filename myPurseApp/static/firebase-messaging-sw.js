importScripts('https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/10.12.2/firebase-messaging.js');

const firebaseConfig = {
  apiKey: "AIzaSyD2Oa58ftspj-9LsrKG5R7WovWleE2sQ5o",
  authDomain: "my-purse-b5a82.firebaseapp.com",
  projectId: "my-purse-b5a82",
  storageBucket: "my-purse-b5a82.appspot.com",
  messagingSenderId: "599515776259",
  appId: "1:599515776259:web:9e43560aac446852b51536",
  measurementId: "G-G7LTEP5Q9R"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

const messaging = firebase.messaging();

// Handle background messages
messaging.onBackgroundMessage(payload => {
  console.log('[firebase-messaging-sw.js] Received background message ', payload);
  const notificationTitle = payload.notification.title;
  const notificationOptions = {
    body: payload.notification.body,
    icon: payload.notification.icon
  };

  self.registration.showNotification(notificationTitle, notificationOptions);
});