const functions = require("firebase-functions");
const { PubSub } = require("@google-cloud/pubsub");

const pubsub = new PubSub();

exports.scheduler = functions.pubsub
  .schedule("every 5 minutes") // At midnight.
  .timeZone("Asia/Bangkok")
  .onRun(async (_) => {
    const n = Math.floor(Math.random() * 31);
    console.log(n);
    const topic = pubsub.topic("fibonacci");
    const message = {
      data: n,
    };
    await topic.publish(Buffer.from(JSON.stringify(message), "utf-8"));
  });
