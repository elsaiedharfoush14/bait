# Firestore security rules (he pastes them in Firebase console → Firestore → Rules)

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /families/{fid} {
      allow get: if request.auth != null && fid.size() >= 20;
      allow create, update: if request.auth != null && fid.size() >= 20
        && request.resource.data.keys().hasOnly(['d','u'])
        && request.resource.data.d is string && request.resource.data.d.size() < 900000;
    }
  }
}
```
