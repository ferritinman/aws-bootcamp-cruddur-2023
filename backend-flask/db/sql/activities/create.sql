INSERT INTO activities (
    user_uuid,
    message,
    expires_at
) VALUES (
    (SELECT uuid FROM users WHERE users.cognito_user_id = %(cognito_user_id)s),
    %(message)s,
    %(expires_at)s
) RETURNING uuid;