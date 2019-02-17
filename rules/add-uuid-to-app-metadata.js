function (user, context, callback) {
  // Generates a version 4 random UUID. Namespace UUIDs do not appear
  // to be an option in Auth0 at this time.
  const uuid = require('uuid@3.3.2');
  //const uuidv5 = require('uuid@3.3.2/v5');


  user.app_metadata = user.app_metadata || {};
  user.app_metadata.uuid = user.app_metadata.uuid || uuid();
  //user.app_metadata.uuid = uuidv5(user.user_id, configuration.uuid_namespace);
  
  auth0.users.updateAppMetadata(user.user_id, user.app_metadata)
    .then(function(){
    callback(null, user, context);
  })
    .catch(function(err){
    callback(err);
  });
}
