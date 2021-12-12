import sys
import re

class DecoderTokenizer():
    def __init__(self, refTokenizer):
        self.refTokenizer = refTokenizer

        self.byte_decoder = {v: k for k, v in self.bytes_to_unicode().items()}

    def convertSentToIds(self, sent, refSent):
        sent = sent.replace('взять(', ' 3 ').replace(')взять', ' 4 ').replace('движение(обратно)движение', ' 7 ').replace('движение(', ' 5 ').replace(')движение', ' 6 ')
        toks = re.sub(r'\s+', ' ', sent).strip().split(' ')

        for i in range(len(toks)):
            if toks[i] == '7':
                toks[i] = [int(toks[i])]
                continue

            if toks[i] == '3' or toks[i] == '5':
                toks[i] = [int(toks[i])]
                continue

            if toks[i] == '4' or toks[i] == '6':
                toks[i] = [int(toks[i])]
                continue

            toks[i] = self.refTokenizer.convertTokenToIds(toks[i])

        toks[:] = [1] + [item for sublist in toks for item in sublist] + [2]

        for i in range(len(toks)):
            for j in range(len(refSent)):
                if refSent[j] == toks[i] and refSent[j] > 9:
                    toks[i] = j+10

        return toks

    def bytes_to_unicode(self):
        """
        Returns list of utf-8 byte and a corresponding list of unicode strings.
        The reversible bpe codes work on unicode strings.
        This means you need a large # of unicode characters in your vocab if you want to avoid UNKs.
        When you're at something like a 10B token dataset you end up needing around 5K for decent coverage.
        This is a signficant percentage of your normal, say, 32K bpe vocab.
        To avoid that, we want lookup tables between utf-8 bytes and unicode strings.
        And avoids mapping to whitespace/control characters the bpe code barfs on.
        """
        _chr = unichr if sys.version_info[0] == 2 else chr
        bs = list(range(ord("!"), ord("~")+1))+list(range(ord("¡"), ord("¬")+1))+list(range(ord("®"), ord("ÿ")+1))
        cs = bs[:]
        n = 0
        for b in range(2**8):
            if b not in bs:
                bs.append(b)
                cs.append(2**8+n)
                n += 1
        cs = [_chr(n) for n in cs]
        return dict(zip(bs, cs))

    def convertIdsToSent(self, ids, refSent):
        tokens = ['взять(', ')взять', 'движение(', ')движение', 'движение(обратно)движение']
        output=[]

        for i in range(len(ids)):
            if ids[i]>2 and ids[i]<10:
                output.append(tokens[ids[i]-3])
            else:
                if ids[i] - 10 < len(refSent)-1:
                    if ids[i] > 2:
                        ids[i] = refSent[ids[i] - 10]

                    idToWords = bytearray([self.byte_decoder[c] for c in self.refTokenizer.convertIdsToSent(ids[i])]).decode('utf-8')
                    output.append(idToWords)

        # output = ''.join(output)
        # output = re.sub('(\d+)([а-яА-Яa-zA-Z])', r'\1 \2', output)
        # output = re.sub('([а-яА-Яa-zA-Z])(\d+)', r'\1 \2', output)
        # output = re.sub('\s+', r' ', output).strip()

        return output
