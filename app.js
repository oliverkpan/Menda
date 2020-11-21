var firebase = require("firebase/app");

require("firebase/database")
require("firebase/auth")

var firebaseConfig = {
    apiKey: "AIzaSyBDPB89itGMDiZgksfiOtOmT0kJ4FMBul4",
    authDomain: "hack-western-7.firebaseapp.com",
    databaseURL: "https://hack-western-7.firebaseio.com",
    projectId: "hack-western-7",
    storageBucket: "hack-western-7.appspot.com",
    messagingSenderId: "1061541009957",
    appId: "1:1061541009957:web:4382341cb8637e3128fdcc"
  };
// Initialize Firebase
firebase.initializeApp(firebaseConfig);

let db = firebase.database().ref()

let object = {date: "today", emotion: "happy", experience: "worked all day"}

db.child('logs').push(object)
