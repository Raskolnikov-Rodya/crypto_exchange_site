#!/usr/bin/env python3
"""Promote or create an admin user for local/staging environments."""

from __future__ import annotations

import argparse
import asyncio

from sqlalchemy import select

from App.core.security import get_password_hash, validate_password_strength
from App.database import AsyncSessionLocal
from App.models.user import Role, User


async def bootstrap_admin(email: str, password: str, username: str | None, phone: str | None) -> None:
    validate_password_strength(password)

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if user is None:
            user = User(
                email=email,
                username=username,
                phone=phone,
                hashed_password=get_password_hash(password),
                role=Role.ADMIN,
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            print(f"Created admin user: id={user.id} email={user.email}")
            return

        user.role = Role.ADMIN
        if username:
            user.username = username
        if phone:
            user.phone = phone
        user.hashed_password = get_password_hash(password)
        await session.commit()
        print(f"Updated existing user to admin: id={user.id} email={user.email}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create or promote an admin user")
    parser.add_argument("--email", required=True, help="Admin email")
    parser.add_argument("--password", required=True, help="Admin password")
    parser.add_argument("--username", default=None, help="Optional username")
    parser.add_argument("--phone", default=None, help="Optional phone")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(bootstrap_admin(args.email, args.password, args.username, args.phone))
