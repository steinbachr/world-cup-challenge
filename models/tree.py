class ProbableTournamentTree():
    """
    the probable tournament tree details the likely winners of games from the round of 16 on
    """
    MAX_LEVEL = 4

    class Node():
        def __init__(self, left, right, winner=None):
            self.left = left
            self.right = right
            self.winner = winner

        def children_winner(self):
            """
            :return: ``Team`` instance. The winner of this ``Node``'s left and right children
            """
            left_winning_prob = self.left.winner.winning_probabilities[self.right.winner.country]
            return self.left.winner if left_winning_prob >= .5 else self.right.winner

    def __init__(self, tournament):
        self.tournament = tournament
        self.groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.group_pointer = 0
        self.group_subpointer = 0
        self.root = self.build_tree(self.Node(None, None))

    def _search_subtree(self, subtree, team):
        """
        :param subtree: ``Node`` instance, the subtree to search
        :param team: ``Team`` instance, the team to search ``subtree`` for
        :return: ``True`` if ``team`` in ``subtree``. ``False`` o/w
        """
        if subtree.winner.country == team.country:
            return True
        elif subtree.left is None or subtree.right is None:
            return False
        else:
            return self._search_subtree(subtree.left, team) or self._search_subtree(subtree.right, team)

    def build_tree(self, node, cur_level=MAX_LEVEL):
        """
        :param node: the current root of the tree being built
        :return: ``Node`` the original node fed into the method completely built into a tree
        """
        if cur_level == 0:
            node.left = None
            node.right = None

            # the leafs value should be the winner of the group pointed to by self.group_pointer
            group = self.groups[self.group_pointer % len(self.groups)]
            group_winners = self.tournament.get_group_winners(group)

            # 1st place from group should play 2nd place from sibling group
            node.winner = group_winners[self.group_subpointer]
            self.group_pointer += 1
            # make sure that we invert the order of choosing 1st place / 2nd place after traversing all groups once
            self.group_subpointer = 1 if self.group_subpointer == 0 or self.group_pointer == len(self.groups) else 0
        else:
            node.left = self.build_tree(self.Node(None, None), cur_level=cur_level - 1)
            node.right = self.build_tree(self.Node(None, None), cur_level=cur_level - 1)
            node.winner = node.children_winner()

        return node

    def get_opponent_at_stage(self, team, stage):
        """
        :param team: ``Team`` instance to get the probable opponent for
        :param stage: ``int`` the stage to get the probable opponent for ``team`` at. (Stage should always be between
        0 inclusive and 3 exclusive)
        :return: ``Team`` instance the ``team``'s likely opponent at ``stage``

        This method has two distinct paths depending on whether ``team`` is a part of the probability tree or not.
        If not, it means it's likely they won't make it out of group, so to get their likely opponent at ``stage``,
        we emulate the team in their group who came in second and find that team's opponent at ``stage``. If ``team`` is
        already in the tree, the method is more straightforward.
        """
        def _helper(node, t=None, cur_level=self.MAX_LEVEL):
            deeper_level = cur_level - 1
            if deeper_level < 0:
                return None
            elif deeper_level == stage:
                # if the next level is the one that we're looking for, then get the subtree (left or right) that the
                # team we're searching for is in and return the direct child from the opposite subtree, this is their
                # opponent
                if self._search_subtree(node.left, t):
                    return node.right.winner
                elif self._search_subtree(node.right, t):
                    return node.left.winner
                else:
                    return None
            else:
                return _helper(node.left, t=t, cur_level=deeper_level) or _helper(node.right, t=t, cur_level=deeper_level)

        group_winners = self.tournament.get_group_winners(team.group)
        return _helper(self.root, t=team if team in group_winners else group_winners[1])

    def print_tree(self):
        """
        print this tree to STDOUT
        """
        levels = {}

        def _helper(node, cur_depth=0):
            vals_at_level = levels.get(cur_depth, [])
            vals_at_level.append(node.winner.country)
            levels[cur_depth] = vals_at_level

            if node.left is None or node.right is None:
                return
            else:
                _helper(node.right, cur_depth=cur_depth + 1)
                _helper(node.left, cur_depth=cur_depth + 1)

        _helper(self.root)
        for level in levels.keys():
            print "\t".join(levels[level])
            print "\n"