import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates


# time作为索引
df = pd.read_csv("./count.csv", index_col=None, parse_dates=True, names=["total"], dtype={"total": np.int64}, encoding="utf-8")
increment = df['total'].diff()
df["increment"] = increment
fig, ax = plt.subplots()
fig.set_size_inches(12, 6)


# ax.plot_date(df.index.to_pydatetime(), df["total"], 'v-')
# # ax.plot_date(df["time"], df["total"], 'v-')
# ax.xaxis.set_minor_locator(dates.HourLocator())
# ax.xaxis.set_minor_formatter(dates.DateFormatter('\n%H:%M'))
# ax.xaxis.grid(True, which="minor")
# ax.yaxis.grid()
# ax.xaxis.set_major_locator(dates.DayLocator())
# ax.xaxis.set_major_formatter(dates.DateFormatter('%m-%d'))
#
# plt.tight_layout()
# plt.show()

df_recent = df[-60:]
print()
increment_mean = df_recent["increment"].mean()
ax.plot_date(df_recent.index.to_pydatetime(), df_recent["increment"], 'o-')
# ax.plot_date(df["time"], df["total"], 'v-')
ax.xaxis.set_minor_locator(dates.MinuteLocator(interval=10))
ax.xaxis.set_minor_formatter(dates.DateFormatter('\n%H:%M'))
ax.xaxis.grid(True, which="minor")
ax.yaxis.grid()
ax.xaxis.set_major_locator(dates.DayLocator())
ax.xaxis.set_major_formatter(dates.DateFormatter('%m-%d'))
# axvline 竖直  axhline 横向
ax.axhline(35, ls="--", color="red")
ax.axhline(increment_mean, ls="--", color="blue")

ax.annotate('local max', xy=(20, 20), xytext=(5, 5),
            arrowprops=dict(facecolor='black', shrink=1),
            )
plt.savefig("result.png")
plt.tight_layout()
# plt.show()
