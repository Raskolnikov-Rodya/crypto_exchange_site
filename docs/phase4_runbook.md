# Phase 4 Hardening Runbook & Checklist

## Purpose
Operational checklist before any public beta exposure.

## 1) Environment & Secrets
- [ ] `ENV=production` only in production deployments.
- [ ] `JWT_SECRET` set to strong secret (>= 32 chars).
- [ ] Database URL uses production credentials and TLS where available.
- [ ] No default secrets in deployed env files.

## 2) Auth-Sensitive Rate Limiting
- [ ] Login endpoint protected with rate limiter.
- [ ] Registration endpoint protected with rate limiter.
- [ ] Limits validated against expected traffic profile.
- [ ] For scale-out: migrate limiter backing store to Redis.

## 3) Admin Financial Auditability
- [ ] Manual credit action emits audit log.
- [ ] Withdrawal approve/reject/complete emit audit logs.
- [ ] Logs retained and exportable for incident review.

## 4) Backup & Recovery
- [ ] Nightly PostgreSQL dumps enabled.
- [ ] Off-site backup copy configured.
- [ ] Restore procedure tested in non-production environment.
- [ ] Recovery point objective (RPO) and recovery time objective (RTO) documented.

## 5) Smoke Verification Before Release
- [ ] Register + login works.
- [ ] User balance fetch works.
- [ ] Withdrawal request + admin approval/rejection/completion works.
- [ ] Matching endpoint executes and updates balances/transactions.

## Suggested Backup Commands (example)
```bash
# Backup
pg_dump -h <host> -U <user> -d <db> -F c -f backup_$(date +%F).dump

# Restore
pg_restore -h <host> -U <user> -d <db> --clean --if-exists backup_YYYY-MM-DD.dump
```
