print('Start #################################################################');
db = db.getSiblingDB('entity_mgmt_db');
db.createUser(
  {
    user: 'mongoadmin',
    pwd: 'password',
    roles: [{ role: 'readWrite', db: 'entity_mgmt_db' }],
  },
);
db.createCollection('application_status');
db.application_status.insertOne({
  'status': 'alive'
});

db = db.getSiblingDB('booking_mgmt_db');
db.createUser(
  {
    user: 'mongoadmin',
    pwd: 'password',
    roles: [{ role: 'readWrite', db: 'booking_mgmt_db' }],
  },
);
db.createCollection('application_status');
db.application_status.insertOne({
  'status': 'alive'
});
print('END #################################################################');