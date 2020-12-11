function (user, context, callback) {
  // Generates a version 4 random UUID. Namespace UUIDs do not appear
  // to be an option in Auth0 at this time.
  const { v4: uuidv4 } = require('uuid');

  user.app_metadata = user.app_metadata || {};
  user.app_metadata.uuid = user.app_metadata.uuid || uuid();
  
  auth0.users.updateAppMetadata(user.user_id, user.app_metadata)
    .then(function(){
    callback(null, user, context);
  })
    .catch(function(err){
    callback(err);
  });
}
