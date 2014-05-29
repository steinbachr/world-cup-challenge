class ProbableTournamentTree():
    """
    the probable tournament tree details the likely winners of games from the round of 16 on
    """
    MAX_LEVEL = 4

    class Node():
        def __init__(self, left, right, winner=None, group_possibilities=''):
            self.left = left
            self.right = right
            self.winner = winner
            self.group_possibilities = group_possibilities

        def children_winner(self):
            """
            :return: ``Team`` instance. The winner of this ``Node``'s left and right children
            """
            left_winning_prob = self.left.winner.winning_probabilities[self.right.winner.country]
            return self.left.winner if left_winning_prob >= .5 else self.right.winner

        def concatenated_children_groups(self):
            """
            :return: ``str`` the concatenated groups of the direct descendants of this Node, or None if no descendants
            exist
            """
            if self.left and self.right:
                return self.left.group_possibilities + self.right.group_possibilities
            else:
                return None

    def __init__(self, tournament):
        self.tournament = tournament
        self.groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.group_pointer = 0
        self.root = self.build_tree(self.Node(None, None))

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

            # take the first place group winners for the first leaves, then take the runner-ups
            node.winner = group_winners[0 if self.group_pointer < len(self.groups) else 1]
            node.group_possibilities = group
            self.group_pointer += 1
        else:
            node.left = self.build_tree(self.Node(None, None), cur_level=cur_level - 1)
            node.right = self.build_tree(self.Node(None, None), cur_level=cur_level - 1)
            node.winner = node.children_winner()
            node.group_possibilities = node.concatenated_children_groups()

        return node

    def get_opponent_at_stage(self, team, stage):
        """
        :param team: ``Team`` instance to get the probable opponent for
        :param stage: ``int`` the stage to get the probable opponent for ``team`` at. (Stage should always be between
        0 inclusive and 3 exclusive)
        :return: ``Team`` instance the ``team``'s likely opponent at ``stage``
        """
        def _helper(node, cur_level=self.MAX_LEVEL):
            deeper_level = cur_level - 1
            if deeper_level < 0:
                return None
            elif deeper_level == stage:
                # if the next level is the one that we're looking for, then get the child node which
                # represents the group of ``team``'s sibling (which is the teams opponent)
                if team.group in node.left.group_possibilities:
                    return node.right.winner
                else:
                    return node.left.winner
            else:
                return _helper(node.left, cur_level=deeper_level) or _helper(node.right, cur_level=deeper_level)
        return _helper(self.root)

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