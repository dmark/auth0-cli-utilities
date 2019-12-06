function (user, context, callback) {
  var namespace = "https://leanangle.io/claims/";
  user.user_metadata = user.user_metadata || {};
  context.idToken[namespace + "user_metadata"] = user.user_metadata; 
  callback(null, user, context);
}