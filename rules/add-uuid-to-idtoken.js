function (user, context, callback) {
  var namespace = "https://leanangle.io/claims/";
  
  user.app_metadata = user.app_metadata || {};
  user.app_metadata.uuid = user.app_metadata.uuid || {};
  
  context.idToken[namespace + "uuid"] = user.app_metadata.uuid;
  
  callback(null, user, context);
}
