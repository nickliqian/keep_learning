
def count_bonus(A2B):
    items = []
    for i in range(1, 11):
        for j in range(1, 11):
            for k in range(1, 11):
                # 注数
                win_multiple, draw_multiple, loss_multiple = i, j, k
                # 成本
                cost = (win_multiple + draw_multiple + loss_multiple)*2
                # 奖金
                win_bonus = A2B["win"]*win_multiple*2
                draw_bonus = A2B["draw"]*draw_multiple*2
                loss_bonus = A2B["loss"]*loss_multiple*2
                # 盈利
                result_win = win_bonus - cost
                result_draw = draw_bonus - cost
                result_loss = loss_bonus - cost
                # 盈利最大值&最小值
                earn = max(result_win,result_draw,result_loss)
                deficit = min(result_win,result_draw,result_loss)
                # 盈亏比例
                rate = round(deficit/earn, 2)

                item = {
                    "count": (win_multiple, draw_multiple, loss_multiple,),
                    "rate": rate,
                }
                items.append(item)

                print("注数：{}/{}/{} 成本：{:.2f} 奖金：{:.2f}/{:.2f}/{:.2f} 盈利：{:.2f}/{:.2f}/{:.2f} 盈利最大：{:.2f} 盈利最小：{:.2f} 盈亏比例：{:.2f}%"
                      .format(win_multiple, draw_multiple, loss_multiple,
                              cost,
                              win_bonus, draw_bonus, loss_bonus,
                              result_win, result_draw, result_loss,
                              earn,
                              deficit,
                              rate*100))
    r = sorted(items, key=lambda x: x["rate"], reverse=True)
    for i in r:
        print(i)


def main():
    A2B = {
        "A_name": "Panama",
        "B_name": "England",
        "win": 6.9,
        "draw": 4.10,
        "loss": 1.35,
    }

    count_bonus(A2B)


if __name__ == '__main__':
    main()