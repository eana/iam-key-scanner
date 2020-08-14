#!/usr/bin/python3

import datetime, boto3

IAM = boto3.client("iam")
days = 90
svc_accounts = ["svc_user1", "svc_user2", "svc_user3"]


def access_key(user):
    access_keys = {"username": user, "keys": [], "date": []}
    key_details = IAM.list_access_keys(UserName=user)

    # Some user may have 2 access keys. So iterating over them and listing the
    # details of active access key.
    for keys in key_details["AccessKeyMetadata"]:
        if keys["Status"] == "Active" and time_diff(keys["CreateDate"]) >= days:
            access_keys["keys"].append(
                {"id": keys["AccessKeyId"], "time_diff": time_diff(keys["CreateDate"])}
            )

    return access_keys


def time_diff(keycreatedtime):
    # Getting the current time in utc format
    now = datetime.datetime.now(datetime.timezone.utc)

    # Calculating diff between two datetime objects.
    diff = now - keycreatedtime

    # Returning the difference in days
    return diff.days


if __name__ == "__main__":
    # This returns a dictionary response
    details = IAM.list_users(MaxItems=300)

    access_keys = [access_key(X["UserName"]) for X in details["Users"]]

    for user in access_keys:
        if user["username"] not in svc_accounts:
            for key in user["keys"]:
                print(user["username"], key["id"], key["time_diff"], sep=",")
                # deactivate_keys = IAM.update_access_key (AccessKeyId=key['id'], Status='Inactive', UserName=user['username'])
