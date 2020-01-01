#!usr/bin/env python 3
import datetime

from utils.utils import run_file_format


async def complete_chore(ctx, invoker_id, chore_id):
    chore_data = run_file_format(
        "sql/find_incomplete_chore.sql", guild_id=ctx.message.guild.id, chore_id=chore_id,
    )
    if not chore_data:
        await ctx.message.add_reaction("❓")
        return False
    asignee_id = chore_data[0]["user_id"]
    assigned_date = chore_data[0]["assigned_date"]
    completed_date = datetime.datetime.now()
    time_taken = int((completed_date - assigned_date).total_seconds())
    if invoker_id == asignee_id:
        print("...match")
        kwargs = {
            "guild_id": ctx.message.guild.id,
            "completed_date": completed_date,
            "chore_id": chore_id,
            "time_taken": time_taken,
        }
        run_file_format("sql/complete_chore.sql", **kwargs)
        await ctx.message.add_reaction("✅")
        return True
    else:
        await ctx.message.add_reaction("❌")
        return False
