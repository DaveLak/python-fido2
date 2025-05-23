# Copyright (c) 2013 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


from __future__ import absolute_import, unicode_literals

import unittest
from binascii import a2b_hex

from fido2 import cbor, cose
from fido2.cose import ES256, ESP256, RS256, CoseKey, Ed25519, EdDSA, UnsupportedKey

_ES256_KEY = a2b_hex(
    b"A5010203262001215820A5FD5CE1B1C458C530A54FA61B31BF6B04BE8B97AFDE54DD8CBB69275A8A1BE1225820FA3A3231DD9DEED9D1897BE5A6228C59501E4BCD12975D3DFF730F01278EA61C"  # noqa E501
)
_ESP256_KEY = _ES256_KEY[0:4] + a2b_hex("28") + _ES256_KEY[5:]
_RS256_KEY = a2b_hex(
    b"A401030339010020590100B610DCE84B65029FAE24F7BF8A1730D37BC91435642A628E691E9B030BF3F7CEC59FF91CBE82C54DE16C136FA4FA8A58939B5A950B32E03073592FEC8D8B33601C04F70E5E2D5CF7B4E805E1990EA5A86928A1B390EB9026527933ACC03E6E41DC0BE40AA5EB7B9B460743E4DD80895A758FB3F3F794E5E9B8310D3A60C28F2410D95CF6E732749A243A30475267628B456DE770BC2185BBED1D451ECB0062A3D132C0E4D842E0DDF93A444A3EE33A85C2E913156361713155F1F1DC64E8E68ED176466553BBDE669EB82810B104CB4407D32AE6316C3BD6F382EC3AE2C5FD49304986D64D92ED11C25B6C5CF1287233545A987E9A3E169F99790603DBA5C8AD2143010001"  # noqa E501
)
_EdDSA_KEY = a2b_hex(
    b"a4010103272006215820ee9b21803405d3cf45601e58b6f4c06ea93862de87d3af903c5870a5016e86f5"  # noqa E501
)
_Ed25519_KEY = _EdDSA_KEY[0:4] + a2b_hex("32") + _EdDSA_KEY[5:]


class TestCoseKey(unittest.TestCase):
    def test_ES256_parse_verify(self):
        key = CoseKey.parse(cbor.decode(_ES256_KEY))
        self.assertIsInstance(key, ES256)
        self.assertEqual(
            key,
            {
                1: 2,
                3: -7,
                -1: 1,
                -2: a2b_hex(
                    b"A5FD5CE1B1C458C530A54FA61B31BF6B04BE8B97AFDE54DD8CBB69275A8A1BE1"
                ),
                -3: a2b_hex(
                    b"FA3A3231DD9DEED9D1897BE5A6228C59501E4BCD12975D3DFF730F01278EA61C"
                ),
            },
        )
        key.verify(
            a2b_hex(
                b"0021F5FC0B85CD22E60623BCD7D1CA48948909249B4776EB515154E57B66AE12010000002C"  # noqa E501
                + b"7B89F12A9088B0F5EE0EF8F6718BCCC374249C31AEEBAEB79BD0450132CD536C"
            ),
            a2b_hex(
                b"304402202B3933FE954A2D29DE691901EB732535393D4859AAA80D58B08741598109516D0220236FBE6B52326C0A6B1CFDC6BF0A35BDA92A6C2E41E40C3A1643428D820941E0"  # noqa E501
            ),
        )

    def test_ESP256_parse_verify(self):
        key = CoseKey.parse(cbor.decode(_ESP256_KEY))
        self.assertIsInstance(key, ESP256)
        self.assertEqual(
            key,
            {
                1: 2,
                3: -9,
                -1: 1,
                -2: a2b_hex(
                    b"A5FD5CE1B1C458C530A54FA61B31BF6B04BE8B97AFDE54DD8CBB69275A8A1BE1"
                ),
                -3: a2b_hex(
                    b"FA3A3231DD9DEED9D1897BE5A6228C59501E4BCD12975D3DFF730F01278EA61C"
                ),
            },
        )
        key.verify(
            a2b_hex(
                b"0021F5FC0B85CD22E60623BCD7D1CA48948909249B4776EB515154E57B66AE12010000002C"  # noqa E501
                + b"7B89F12A9088B0F5EE0EF8F6718BCCC374249C31AEEBAEB79BD0450132CD536C"
            ),
            a2b_hex(
                b"304402202B3933FE954A2D29DE691901EB732535393D4859AAA80D58B08741598109516D0220236FBE6B52326C0A6B1CFDC6BF0A35BDA92A6C2E41E40C3A1643428D820941E0"  # noqa E501
            ),
        )

    def test_RS256_parse_verify(self):
        key = CoseKey.parse(cbor.decode(_RS256_KEY))
        self.assertIsInstance(key, RS256)
        self.assertEqual(
            key,
            {
                1: 3,
                3: -257,
                -1: a2b_hex(
                    b"B610DCE84B65029FAE24F7BF8A1730D37BC91435642A628E691E9B030BF3F7CEC59FF91CBE82C54DE16C136FA4FA8A58939B5A950B32E03073592FEC8D8B33601C04F70E5E2D5CF7B4E805E1990EA5A86928A1B390EB9026527933ACC03E6E41DC0BE40AA5EB7B9B460743E4DD80895A758FB3F3F794E5E9B8310D3A60C28F2410D95CF6E732749A243A30475267628B456DE770BC2185BBED1D451ECB0062A3D132C0E4D842E0DDF93A444A3EE33A85C2E913156361713155F1F1DC64E8E68ED176466553BBDE669EB82810B104CB4407D32AE6316C3BD6F382EC3AE2C5FD49304986D64D92ED11C25B6C5CF1287233545A987E9A3E169F99790603DBA5C8AD"  # noqa E501
                ),
                -2: a2b_hex(b"010001"),
            },
        )
        key.verify(
            a2b_hex(
                b"0021F5FC0B85CD22E60623BCD7D1CA48948909249B4776EB515154E57B66AE12010000002E"  # noqa E501
                + b"CC9340FD84950987BA667DBE9B2C97C7241E15E2B54869A0DD1CE2013C4064B8"
            ),
            a2b_hex(
                b"071B707D11F0E7F62861DFACA89C4E674321AD8A6E329FDD40C7D6971348FBB0514E7B2B0EFE215BAAC0365C4124A808F8180D6575B710E7C01DAE8F052D0C5A2CE82F487C656E7AD824F3D699BE389ADDDE2CBF39E87A8955E93202BAE8830AB4139A7688DFDAD849F1BB689F3852BA05BED70897553CC44704F6941FD1467AD6A46B4DAB503716D386FE7B398E78E0A5A8C4040539D2C9BFA37E4D94F96091FFD1D194DE2CA58E9124A39757F013801421E09BD261ADA31992A8B0386A80AF51A87BD0CEE8FDAB0D4651477670D4C7B245489BED30A57B83964DB79418D5A4F5F2E5ABCA274426C9F90B007A962AE15DFF7343AF9E110746E2DB9226D785C6"  # noqa E501
            ),
        )

    def test_EdDSA_parse_verify(self):
        key = CoseKey.parse(cbor.decode(_EdDSA_KEY))
        self.assertIsInstance(key, EdDSA)
        self.assertEqual(
            key,
            {
                1: 1,
                3: -8,
                -1: 6,
                -2: a2b_hex(
                    "EE9B21803405D3CF45601E58B6F4C06EA93862DE87D3AF903C5870A5016E86F5"
                ),
            },
        )
        key.verify(
            a2b_hex(
                b"a379a6f6eeafb9a55e378c118034e2751e682fab9f2d30ab13d2125586ce1947010000000500a11a323057d1103784ddff99a354ddd42348c2f00e88d8977b916cabf92268"  # noqa E501
            ),
            a2b_hex(
                b"e8c927ef1a57c738ff4ba8d6f90e06d837a5219eee47991f96b126b0685d512520c9c2eedebe4b88ff2de2b19cb5f8686efc7c4261e9ed1cb3ac5de50869be0a"  # noqa E501
            ),
        )

    def test_Ed25519_parse_verify(self):
        key = CoseKey.parse(cbor.decode(_Ed25519_KEY))
        self.assertIsInstance(key, Ed25519)
        self.assertEqual(
            key,
            {
                1: 1,
                3: -19,
                -1: 6,
                -2: a2b_hex(
                    "EE9B21803405D3CF45601E58B6F4C06EA93862DE87D3AF903C5870A5016E86F5"
                ),
            },
        )
        key.verify(
            a2b_hex(
                b"a379a6f6eeafb9a55e378c118034e2751e682fab9f2d30ab13d2125586ce1947010000000500a11a323057d1103784ddff99a354ddd42348c2f00e88d8977b916cabf92268"  # noqa E501
            ),
            a2b_hex(
                b"e8c927ef1a57c738ff4ba8d6f90e06d837a5219eee47991f96b126b0685d512520c9c2eedebe4b88ff2de2b19cb5f8686efc7c4261e9ed1cb3ac5de50869be0a"  # noqa E501
            ),
        )

    def test_unsupported_key(self):
        key = CoseKey.parse({1: 4711, 3: 4712, -1: b"123", -2: b"456"})
        self.assertIsInstance(key, UnsupportedKey)
        self.assertEqual(key, {1: 4711, 3: 4712, -1: b"123", -2: b"456"})

    def test_supported_algs(self):
        self.assertEqual(CoseKey.for_alg(-7), cose.ES256)
        self.assertEqual(CoseKey.for_alg(-8), cose.EdDSA)
        self.assertEqual(CoseKey.for_alg(-9), cose.ESP256)
        self.assertEqual(CoseKey.for_alg(-19), cose.Ed25519)
        self.assertEqual(CoseKey.for_alg(-35), cose.ES384)
        self.assertEqual(CoseKey.for_alg(-36), cose.ES512)
        self.assertEqual(CoseKey.for_alg(-37), cose.PS256)
        self.assertEqual(CoseKey.for_alg(-47), cose.ES256K)
        self.assertEqual(CoseKey.for_alg(-51), cose.ESP384)
        self.assertEqual(CoseKey.for_alg(-52), cose.ESP512)
        self.assertEqual(CoseKey.for_alg(-53), cose.Ed448)
        self.assertEqual(CoseKey.for_alg(-257), cose.RS256)
        self.assertEqual(CoseKey.for_alg(-65535), cose.RS1)
