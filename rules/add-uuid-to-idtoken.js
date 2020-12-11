function (user, context, callback) {
  // recommended namespace is a URL-formatted string
  // var namespace = "https://${YOUR_DOMAIN}/claims/"
  var namespace = "https://sr2.ca/claims/";
  
  user.app_metadata = user.app_metadata || {};
  user.app_metadata.uuid = user.app_metadata.uuid || {};
  
  context.idToken[namespace + "uuid"] = user.app_metadata.uuid;
  
  callback(null, user, context);
}
