function (user, context, callback) {
  user.user_metadata = user.user_metadata || {};
  user.user_metadata.first_name = user.user_metadata.first_name || '';
  user.user_metadata.lastName = user.user_metadata.lastName || '';
  if (typeof user.user_metadata.first_name !== 'undefined' && typeof user.user_metadata.given_name === 'undefined') {
    user.user_metadata.given_name = user.user_metadata.first_name;
  }
  if (typeof user.user_metadata.lastName !== 'undefined' && typeof user.user_metadata.family_name === 'undefined') {
    user.user_metadata.family_name = user.user_metadata.lastName;
  }

  auth0.users.updateUserMetadata(user.user_id, user.user_metadata)
    .then(function(){
        callback(null, user, context);
    })
    .catch(function(err){
        callback(err);
    });
}
