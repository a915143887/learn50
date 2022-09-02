import unittest
class CheckPoint(unittest.TestCase):
    def __init__(self,  methodName='runTest'):
        super(CheckPoint, self).__init__(methodName)
        self._testMethodName = methodName
        self.flag = 0
        self.msg = []

    # 基本的布尔断言：要么正确，要么错误的验证
    def checkAssertEqual(self, arg1, arg2, msg=None):
        try:
            self.assertEqual(arg1, arg2, msg)
        except Exception as e:
            self.flag += 1
            self.msg.append("\n{}".format(msg))
            print(e)

    def checkAssertNotEqual(self, arg1, arg2, msg=None):
        try:
            self.assertNotEqual(arg1, arg2, msg)
        except Exception as e:
            self.flag += 1
            self.msg.append("\n{}".format(msg))
            print(e)

    def checkAssertTrue(self, expr, msg=None):
        """验证expr是true，如果为false，则fail"""
        try:
            self.assertTrue(expr, msg)
        except Exception as e:
            self.flag += 1
            self.msg.append("\n{}".format(msg))
            print(e)

    def checkAssertFalse(self, expr, msg=None):
        try:
            self.assertFalse(expr, msg)
        except Exception as e:
            self.flag += 1
            self.msg.append("\n{}".format(msg))
            print(e)

    def checkAssertGreater(self, first, second, msg=None):
        """　验证first > second，否则fail"""
        try:
            self.assertGreater(first, second)
        except Exception as e:
            self.flag += 1
            self.msg.append("\n{}".format(msg))
            print(e)

    def checkAssertGreaterEqual(self, first, second, msg=None):
        try:
            self.assertGreaterEqual(first, second)
        except Exception as e:
            self.flag += 1
            self.msg.append("\n{}".format(msg))
            print(e)

    def checkAssertLess(self, first, second, msg=None):
        """验证first < second，否则fail"""
        try:
            self.assertLess(first, second)
        except Exception as e:
            self.flag += 1
            self.msg.append("\n{}".format(msg))
            print(e)

    def checkAssertLessEqual(self, first, second, msg=None):
        """验证first <= second，否则fail"""
        try:
            self.assertLessEqual(first, second)
        except Exception as e:
            self.flag += 1
            self.msg.append("\n{}".format(msg))
            print(e)

    def checkTestResult(self):
        return self.assertEqual(self.flag, 0, "{}".format(self.msg))