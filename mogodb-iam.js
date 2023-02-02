// mongodb.ts
const AWS = require('aws-sdk')
const {MongoClient} = require('mongodb');
const fs = require('fs')
const CLUSTER_NAME = 'stg-common-40.rxoxb'
const webIdentityToken = fs.readFileSync(process.env.AWS_WEB_IDENTITY_TOKEN_FILE,"utf8");
  const sts = new AWS.STS({ region: 'ap-southeast-1' });
  const params = {
    RoleArn: process.env.AWS_ROLE_ARN,
    RoleSessionName: 'session',
    DurationSeconds: 900,
    WebIdentityToken: webIdentityToken
  };
sts.assumeRoleWithWebIdentity(params,function (err,data){
        if (err) {
        console.log(err,err.stack)
        }else {
const AccessKeyId = encodeURIComponent(data.Credentials.AccessKeyId);
const SessionToken = encodeURIComponent(data.Credentials.SessionToken);
const SecretKey = encodeURIComponent(data.Credentials.SecretAccessKey);
const authMechanism = "MONGODB-AWS";
let uri = `mongodb+srv://${AccessKeyId}:${SecretKey}@${CLUSTER_NAME}.mongodb.net/?authSource=%24external&authMechanism=${authMechanism}&authMechanismProperties=AWS_SESSION_TOKEN:${SessionToken}`;
const client = new MongoClient(uri);
async function run() {
  try {
    // Establish and verify connection.
    await client.db("admin").command({ ping: 1 });
    console.log("Connected successfully to server.");
  } finally {
    // Ensure that the client closes when it finishes/errors.
    await client.close();
  }
}
run().catch(console.dir);
}
});
