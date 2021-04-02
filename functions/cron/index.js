const functions = require("firebase-functions");
const { PubSub } = require("@google-cloud/pubsub");

const pubsub = new PubSub();

exports.scheduler = functions.pubsub
  .schedule("every 5 minutes") // At midnight.
  .timeZone("Asia/Bangkok")
  .onRun(async (_) => {
    try {
      const topic = pubsub.topic("fibonacci");
      const message = {
        data: Math.floor(Math.random() * 31),
      };
      await topic.publish(Buffer.from(JSON.stringify(message), "utf-8"));
    } catch (_) {}
  });
