function (user, context, callback) {
  var namespace = "https://sr2.ca/claims/";
  user.user_metadata = user.user_metadata || {};
  context.idToken[namespace + "user_metadata"] = user.user_metadata; 
  callback(null, user, context);
}
