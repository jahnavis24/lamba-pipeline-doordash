# 📦 Serverless Data Processing Pipeline on AWS

This project demonstrates a fully automated, event-driven data pipeline using AWS services like Lambda, S3, CodeBuild, and SNS. It simulates a real-world use case where delivery data is ingested, filtered, and stored — with CI/CD automation and email notifications.

---

## 🎯 Use Case

Process raw delivery JSON files, filter for records where `status = "delivered"`, store the results in a target bucket, and notify the user via email once successful.

---

## 🖼️ Architecture

![Architecture](Screen%20Recording%202025-07-20%20at%203.08.18%E2%80%AFPM.gif)

---

## ⚙️ Workflow Steps

### 1. 👤 Developer

- You push code changes to the GitHub source repository.

### 2. 🔁 Webhook Trigger

- A webhook detects a merge and triggers the CodeBuild pipeline.

### 3. 🧱 AWS CodeBuild

- Builds the Lambda code and uploads the `.zip` to the **Deployment S3 bucket**.
- Pushes a raw JSON file into the **Landing S3 bucket** after a delay.

### 4. 🪣 Amazon S3 Buckets

- `Deployment Bucket`: Stores Lambda deployment zip files.
- `Landing Bucket`: Holds incoming raw delivery JSON files.
- `Target Bucket`: Stores filtered delivery records.

### 5. ⚙️ AWS Lambda (Data Filter)

- Triggered by new files in the Landing bucket.
- Filters for records where `status = "delivered"`.
- Writes filtered data to the **Target bucket**.
- On success, invokes SNS to send a notification.

### 6. 📣 SNS Topic

- Triggered by Lambda after a successful write to Target bucket.
- Publishes a message to subscribers.

### 7. 📧 Email

- The user receives a success notification via email.

---

## 🧪 Tech Stack

- **AWS Lambda** – Filter JSON data
- **Amazon S3** – Raw and processed data storage
- **AWS CodeBuild** – CI/CD for Lambda deployments
- **AWS SNS** – Notification service
- **GitHub** – Source control and webhook integration

---

## 🚀 Highlights

- Fully **serverless** & **event-driven**
- Lightweight and cost-effective (Free Tier eligible)
- Clean architecture using **CI/CD** + automated data processing
- End-to-end visibility with real-time notifications

---

## 📬 Sample Output

```json
[
  {
    "order_id": "12345",
    "status": "delivered",
    "timestamp": "2025-07-19T13:25:43Z"
  }
]
```
