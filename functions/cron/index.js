const functions = require("firebase-functions");
const { PubSub } = require("@google-cloud/pubsub");

const pubsub = new PubSub();

exports.scheduler = functions
  .region("asia-east2")
  .pubsub
  .schedule("every midnight")
  .timeZone("Asia/Bangkok")
  .onRun(async (context) => {
    const n = Math.floor(Math.random() * 31);
    functions.logger.log(n);
    const topic = pubsub.topic("fibonacci");
    const message = {
      data: n,
    };
    await topic.publish(Buffer.from(JSON.stringify(message), "utf-8"));
  });
