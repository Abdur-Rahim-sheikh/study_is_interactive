from sympy import isprime, nsimplify
from pathlib import Path
import csv
from functools import cached_property

class RealNumbers:
    @cached_property
    def getCategories(self):
        path = Path(__file__).parent / "real_numbers.csv"
        with path.open(newline='') as f:
            reader = csv.DictReader(f)
            mp = {}
            for entry in reader:
                mp[entry["category_bangla"]] = entry["definition"]
            
        return mp

        # return {
        #     "বাস্তব সংখ্যা": "ব্যাখ্যা",
        #     "মূলদ": "মূলদ সংখ্যা",
        #     "অমূলদ": "অমূলদ সংখ্যা",
        #     "পূর্ণ": "পূর্ণ সংখ্যা",
        #     "ভগ্নাংশ": "ভগ্নাংশ সংখ্যা",
        #     "ধনাত্মক": "ধনাত্মক সংখ্যা",
        #     "০": "শূন্য সংখ্যা",
        #     "ঋণাত্মক": "ঋণাত্মক সংখ্যা",
        #     "সাধারণ": "সাধারণ সংখ্যা",
        #     "দশমিক": "দশমিক সংখ্যা",
        #     "মৌলিক": "মৌলিক সংখ্যা",
        #     "১": "একক সংখ্যা",
        #     "যৌগিক": "যৌগিক সংখ্যা",
        #     "প্রকৃত": "প্রকৃত সংখ্যা",
        #     "অপ্রকৃত": "অপ্রকৃত সংখ্যা",
        #     "মিশ্র": "মিশ্র সংখ্যা",
        #     "সসীম": "সসীম সংখ্যা",
        #     "অসীম আবৃত্ত": "অসীম আবৃত্ত সংখ্যা",
        #     "অসীম অনাবৃত্ত দশমিক": "অসীম অনাবৃত্ত দশমিক সংখ্যা",
        # }

    @property
    def getFinalCategories(self):
        return [
            "০",
            "ঋণাত্মক",
            "মৌলিক",
            "১",
            "যৌগিক",
            "প্রকৃত",
            "অপ্রকৃত",
            "মিশ্র",
            "সসীম",
            "অসীম আবৃত্ত",
            "অসীম অনাবৃত্ত দশমিক",
        ]

    @property
    def getNumberFormat(self):
        return ["দশমিক", "ভগ্নাংশ", "মিশ্র"]

    @property
    def getGraph(self):
        graph = {}
        graph["বাস্তব সংখ্যা"] = ["মূলদ", "অমূলদ"]
        graph["মূলদ"] = ["পূর্ণ", "ভগ্নাংশ"]
        graph["অমূলদ"] = ["অসীম অনাবৃত্ত দশমিক"]
        graph["পূর্ণ"] = ["ধনাত্মক", "০", "ঋণাত্মক"]
        graph["ভগ্নাংশ"] = ["সাধারণ", "দশমিক"]
        graph["ধনাত্মক"] = ["মৌলিক", "১", "যৌগিক"]
        graph["সাধারণ"] = ["প্রকৃত", "অপ্রকৃত"]
        graph["অপ্রকৃত"] = ["মিশ্র"]
        graph["মিশ্র"] = ["অপ্রকৃত"]
        graph["দশমিক"] = ["সসীম", "অসীম আবৃত্ত"]

        # চেকার
        categories = set(self.getCategories.keys())
        covered = set(graph.keys())
        for key, values in graph.items():
            if key not in categories:
                raise ValueError(f"Key '{key}' not found in categories.")
            for value in values:
                covered.add(value)
                if value not in categories:
                    raise ValueError(f"Value '{value}' not found in categories.")

        if len(covered) != len(categories):
            raise ValueError("Not all categories are covered in the graph.")

        return graph

    def dfs(self, graph, cur, dest):
        return self.__dfs(graph, cur, dest, path=[], visited=set())

    def __dfs(self, graph, cur, dest, path, visited):
        if cur not in self.getCategories or dest not in self.getCategories:
            raise ValueError(f"{cur=} or {dest=} node not found in categories.")

        visited.add(cur)
        path.append(cur)
        if cur == dest:
            return path.copy()

        for neighbor in graph.get(cur, []):
            if neighbor not in visited:
                result = self.__dfs(graph, neighbor, dest, path, visited)
                if result:
                    return result

        path.pop()
        return None

    def is_infinite_decimal(self, value: float):
        number = nsimplify(value)
        if not number.is_rational:
            return True

        num, denum = number.as_numer_denom()

        rem = num % denum
        rems = set()
        cnt = 0
        while rem != 0 and cnt < 1000:
            cnt += 1
            rem = (rem * 10) % denum
            if rem in rems:
                return True
            rems.add(rem)
        return cnt < 1000

    def categorize(self, value: float, apostrophe=False, number_format=None):
        f"""
        যদি number_format দেয়া হয় {self.getNumberFormat}  তাহলে বেস্ট ম্যাচ পাথ রিটার্ন করা হবে
        """
        if number_format and number_format not in self.getNumberFormat:
            raise ValueError(
                f"Invalid number format: {number_format}. Choose from {self.getNumberFormat}."
            )

        try:
            number = nsimplify(value)
        except (ValueError, TypeError):
            raise ValueError(f"Invalid input: {value} cannot be converted to a number.")

        ROOT = "বাস্তব সংখ্যা"
        paths = []
        if not number.is_rational:
            path = self.dfs(self.getGraph, ROOT, "অসীম অনাবৃত্ত দশমিক")
            paths.append(path)

        elif apostrophe:
            path = self.dfs(self.getGraph, ROOT, "অসীম আবৃত্ত")
            paths.append(path)

        elif number.is_Integer:
            num = int(number)
            if num < 0:
                path = self.dfs(self.getGraph, ROOT, "ঋণাত্মক")
                paths.append(path)
            elif num == 0:
                path = self.dfs(self.getGraph, ROOT, "০")
                paths.append(path)
            elif num == 1:
                path = self.dfs(self.getGraph, ROOT, "১")
                paths.append(path)
            elif isprime(num):
                path = self.dfs(self.getGraph, ROOT, "মৌলিক")
                paths.append(path)
            else:
                path = self.dfs(self.getGraph, ROOT, "যৌগিক")
                paths.append(path)
        else:
            # it's finite fractional now
            if self.is_infinite_decimal(value):
                path = self.dfs(self.getGraph, ROOT, "অসীম আবৃত্ত")
                paths.append(path)
            num, denum = number.as_numer_denom()
            if num < denum:
                path = self.dfs(self.getGraph, ROOT, "প্রকৃত")
                paths.append(path)
            else:
                path = self.dfs(self.getGraph, ROOT, "অপ্রকৃত")
                paths.append(path)
                path = self.dfs(self.getGraph, ROOT, "মিশ্র")
                paths.append(path)

            path = self.dfs(self.getGraph, ROOT, "সসীম")
            paths.append(path)

            if number_format:
                if number_format == "দশমিক":
                    paths = [path for path in paths if path[-2] == "দশমিক"]
                elif number_format == "মিশ্র":
                    paths = [path for path in paths if path[-1] == "মিশ্র"]
                elif number_format == "ভগ্নাংশ":
                    paths = [
                        path
                        for path in paths
                        if path[-1] == "প্রকৃত" or path[-1] == "অপ্রকৃত"
                    ]

        return paths
