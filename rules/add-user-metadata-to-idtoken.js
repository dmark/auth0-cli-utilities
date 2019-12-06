function (user, context, callback) {
  user.user_metadata = user.user_metadata || {};
  context.idToken["https://leanangle.io/claims/usermetadata"] = user.user_metadata; 
  callback(null, user, context);
}