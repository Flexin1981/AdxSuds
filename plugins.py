from suds.plugin import MessagePlugin


class EnvelopeFixer(MessagePlugin):
    """
        This is a patch to reset the body of the soap packet to the correct namespace (same as the header)
    """

    def __init__(self, debug):
        self.debug = debug

    def marshalled(self, context):
        """
            Method that catches all soap packets before they get sent and changes the envelope
            body to match the header.
        :param context:
        :return:
        """
        root = context.envelope.getRoot()
        envelope = root.getChild("Envelope")
        children = envelope.getChildren()
        children[1].setPrefix(children[0].prefix)

        if self.debug >= 1:
            print "====================Begin Sent Packet======================"
            print context.envelope
            print "=====================End Sent Packet======================="

        return context

    def unmarshalled(self, context):
        pass

    def received(self, context):
        if self.debug >= 2:
            print "====================Begin Reply Packet======================"
            print context.reply
            print "=====================End Reply Packet======================="
