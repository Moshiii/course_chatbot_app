import tiktoken

def get_token_count(string):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    num_tokens = len(encoding.encode(string))
    return num_tokens


prompt = '''

from difflib import SequenceMatcher

def string_difference(string1, string2):
    matcher = SequenceMatcher(None, string1, string2)
    match = matcher.find_longest_match(0, len(string1), 0, len(string2))
    diff = string1[match.a: match.a + match.size]
    return diff

string1 = "self.conv_loc = nn.Conv2d(self.feat_channels, 1, 1) self.conv_shape = nn.Conv2d(self.feat_channels, self.num_anchors * 2,1)"
string2 = "self.conv_loc = nn.Conv2d(self.in_channels, 1, 1) self.conv_shape = nn.Conv2d(self.in_channels, self.num_anchors * 2, 1)"

string1_diff = string_difference(string1, string2)
string2_diff = string_difference(string2, string1)

print("string1_diff:", string1_diff)  # Output: "self.feat_channels"
print("string2_diff:", string2_diff)  # Output: "self.in_channels"
'''

print(get_token_count(prompt))