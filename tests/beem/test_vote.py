from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import super
import unittest
from parameterized import parameterized
from pprint import pprint
from beem import Steem
from beem.comment import Comment
from beem.vote import Vote, ActiveVotes, AccountVotes
from beem.instance import set_shared_steem_instance

wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
nodes = ["wss://steemd.pevo.science", "wss://gtg.steem.house:8090", "wss://rpc.steemliberator.com", "wss://rpc.buildteam.io",
         "wss://rpc.steemviz.com", "wss://seed.bitcoiner.me", "wss://steemd.steemgigs.org",
         "wss://steemd.minnowsupportproject.org"]
nodes_appbase = ["https://api.steem.house", "https://api.steemit.com", "wss://appbasetest.timcliff.com"]


class Testcases(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bts = Steem(
            node=nodes,
            nobroadcast=True,
            keys={"active": wif},
        )
        self.appbase = Steem(
            node=nodes_appbase,
            nobroadcast=True,
            keys={"active": wif},
        )
        # from getpass import getpass
        # self.bts.wallet.unlock(getpass())
        set_shared_steem_instance(self.bts)
        self.bts.set_default_account("test")
        self.authorpermvoter = u"@gtg/ffdhu-gtg-witness-log|gandalf"
        self.author = u"gtg"
        self.permlink = u"ffdhu-gtg-witness-log"
        self.voter = u"gandalf"
        self.authorperm = u"@gtg/ffdhu-gtg-witness-log"

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_vote(self, node_param):
        if node_param == "non_appbase":
            bts = self.bts
        else:
            bts = self.appbase
        vote = Vote(self.authorpermvoter, steem_instance=bts)
        self.assertEqual(self.voter, vote["voter"])
        self.assertEqual(self.author, vote["author"])
        self.assertEqual(self.permlink, vote["permlink"])

        vote = Vote(self.voter, authorperm=self.authorperm, steem_instance=bts)
        self.assertEqual(self.voter, vote["voter"])
        self.assertEqual(self.author, vote["author"])
        self.assertEqual(self.permlink, vote["permlink"])
        vote_json = vote.json()
        self.assertEqual(self.voter, vote_json["voter"])
        self.assertEqual(self.voter, vote.voter)
        self.assertTrue(vote.weight >= 0)
        self.assertTrue(vote.sbd >= 0)
        self.assertTrue(vote.rshares >= 0)
        self.assertTrue(vote.percent >= 0)
        self.assertTrue(vote.reputation is not None)
        self.assertTrue(vote.rep is not None)
        self.assertTrue(vote.time is not None)
        vote.refresh()
        self.assertEqual(self.voter, vote["voter"])
        self.assertEqual(self.author, vote["author"])
        self.assertEqual(self.permlink, vote["permlink"])
        vote_json = vote.json()
        self.assertEqual(self.voter, vote_json["voter"])
        self.assertEqual(self.voter, vote.voter)
        self.assertTrue(vote.weight >= 0)
        self.assertTrue(vote.sbd >= 0)
        self.assertTrue(vote.rshares >= 0)
        self.assertTrue(vote.percent >= 0)
        self.assertTrue(vote.reputation is not None)
        self.assertTrue(vote.rep is not None)
        self.assertTrue(vote.time is not None)

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_activevotes(self, node_param):
        if node_param == "non_appbase":
            bts = self.bts
        else:
            bts = self.appbase
        votes = ActiveVotes(self.authorperm, steem_instance=bts)
        votes.printAsTable()

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_accountvotes(self, node_param):
        if node_param == "non_appbase":
            bts = self.bts
        else:
            bts = self.appbase
        votes = AccountVotes(self.author, steem_instance=bts)
        self.assertTrue(len(votes) > 0)
        self.assertTrue(isinstance(votes[0], Vote))