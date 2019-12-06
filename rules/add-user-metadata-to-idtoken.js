function (user, context, callback) {
  user.app_metadata = user.app_metadata || {};
  context.idToken["https://leanangle.io/claims/usermetadata"] = user.user_metadata; 
  callback(null, user, context);
}