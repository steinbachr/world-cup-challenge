from populators.teams_populator import TeamsPopulator
import pdb


class TournamentPopulator():
    """
    The group distribution tree is the tricky part of this class and basically just details
    which groups play which groups at the various stages of the tournament
    """
    class GroupDistributionTree():
        MAX_LEVEL = 3

        class Node():
            def __init__(self, left, right, val=None):
                self.left = left
                self.right = right
                self.val = val

            def concatenated_descendant_vals(self):
                """
                :return: ``str`` the concatenated vals of the direct descendants of this Node, or None if no descendants
                exist
                """
                if self.left and self.right:
                    return self.left.val + self.right.val
                else:
                    return None

        def __init__(self):
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
                node.val = self.groups[self.group_pointer % len(self.groups)]
                self.group_pointer += 1
            else:
                node.left = self.build_tree(self.Node(None, None), cur_level=cur_level - 1)
                node.right = self.build_tree(self.Node(None, None), cur_level=cur_level - 1)
                node.val = node.concatenated_descendant_vals()

            return node

        def get_opponents_group_at_stage(self, team, stage):
            """
            :param team: ``Team`` instance to get the probable opponent for
            :param stage: ``int`` the stage to get the probable opponent for ``team`` at. (Stage should always be between
            0 inclusive and 3 exclusive)
            :return: ``str`` group letter (or combination of letters) which represent the group (or combination of groups)
            that ``team`` will be playing at ``stage``
            """
            def _helper(node, cur_level=self.MAX_LEVEL):
                deeper_level = cur_level - 1
                if deeper_level < 0:
                    return None
                elif deeper_level == stage:
                    # if the next level is the one that we're looking for, then get the child node which
                    # represents the group of ``team``'s sibling (which is the teams opponent)
                    if team.group in node.left.val:
                        return node.right.val
                    else:
                        return node.left.val
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
                vals_at_level.append(node.val)
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

    def __init__(self, tournament):
        self.tournament = tournament

    def populate(self):
        self.tournament.teams = TeamsPopulator.populate()
        self.tournament.group_distribution_tree = self.GroupDistributionTree()