from datetime import datetime, timedelta


class Operations:
    date_time_now = datetime.now()

    def largest_prices(self, timestamp_list):
        ids_for_delete = ()
        occur_count = {}  # list of amount of occur
        max_count = [-1, -1]  # largest most occur price
        prior_max_count = [-1, -1]  # lowest most occur price

        for i in timestamp_list:
            if i[1] + timedelta(hours=24) <= self.date_time_now:
                ids_for_delete = ids_for_delete + (i[0],)
                timestamp_list.remove(i)
            else:
                if occur_count.get(i[2], None):
                    occur_count[i[2]] += 1
                else:
                    occur_count[i[2]] = 1
                if occur_count[i[2]] > max_count[1] or (
                    occur_count[i[2]] == max_count[1] and max_count[0] < i[2]
                ):
                    prior_max_count = (
                        max_count
                        if max_count[0] != prior_max_count[0]
                        else prior_max_count
                    )
                    max_count = [i[2], occur_count[i[2]]]

        occur_count.pop(max_count[0])  # exclude max

        for i in occur_count:  # finding prior max
            if occur_count[i] > prior_max_count[1] or (
                occur_count[i] == prior_max_count[1] and prior_max_count[0] < i
            ):
                prior_max_count = [i, occur_count[i]]

        if (
            max_count[0] < prior_max_count[0]
        ):  # if max < prior_max than max = prior_max and vise versa
            max_count[0], prior_max_count[0] = prior_max_count[0], max_count[0]

        return {"max": max_count, "prior_max": prior_max_count, "ids": ids_for_delete}
