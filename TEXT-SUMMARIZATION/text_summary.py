import spacy # spacy model bahasa inggris
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest # mendapatkan n elemen terbesar dari suatu koleksi

text = """Animals are multicellular, eukaryotic organisms in the biological kingdom Animalia. With few exceptions, animals consume organic material, breathe oxygen, have myocytes and are able to move, can reproduce sexually, and grow from a hollow sphere of cells, the blastula, during embryonic development. As of 2022, 2.16 million living animal species have been described—of which around 1.05 million are insects, over 85,000 are molluscs, and around 65,000 are vertebrates. It has been estimated there are around 7.77 million animal species. Animals range in length from 8.5 micrometres (0.00033 in) to 33.6 metres (110 ft). They have complex interactions with each other and their environments, forming intricate food webs. The scientific study of animals is known as zoology.

Most living animal species are in Bilateria, a clade whose members have a bilaterally symmetric body plan. The Bilateria include the protostomes, containing animals such as nematodes, arthropods, flatworms, annelids and molluscs, and the deuterostomes, containing the echinoderms and the chordates, the latter including the vertebrates. Life forms interpreted as early animals were present in the Ediacaran biota of the late Precambrian. Many modern animal phyla became clearly established in the fossil record as marine species during the Cambrian explosion, which began around 539 million years ago. 6,331 groups of genes common to all living animals have been identified; these may have arisen from a single common ancestor that lived 650 million years ago.

Historically, Aristotle divided animals into those with blood and those without. Carl Linnaeus created the first hierarchical biological classification for animals in 1758 with his Systema Naturae, which Jean-Baptiste Lamarck expanded into 14 phyla by 1809. In 1874, Ernst Haeckel divided the animal kingdom into the multicellular Metazoa (now synonymous with Animalia) and the Protozoa, single-celled organisms no longer considered animals. In modern times, the biological classification of animals relies on advanced techniques, such as molecular phylogenetics, which are effective at demonstrating the evolutionary relationships between taxa."""

# fungsi summarizer
def summarizer(rawdocs): 
    stopwords = list(STOP_WORDS)
    print(stopwords)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    print(doc)
    tokens = [token.text for token in doc]
    print(tokens)

    # menghitung banyaknya kemunculan setiap kata
    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1

    print(word_freq)

    # menghitung jumlah kalimat yang dipilih untuk membuat ringkasan
    max_freq = max(word_freq.values())
    print(max_freq)
    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq

    print(word_freq)

    # tokenisasi kalimat
    sent_tokens = [sent for sent in doc.sents]
    print(sent_tokens)

    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent-sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]

    print(sent_scores)

    select_len = int(len(sent_tokens) * 0.3)
    print(select_len)
    summary = nlargest(select_len, sent_scores, key = sent_scores.get)
    print(summary)

    # format hasil ringkasan dengan mengonversi kalimat-kalimat yang terpilih menjadi teks ringkasan
    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)
    print(text)
    print(summary)

    print("Length of original text ", len(text.split(' ')))
    print("Length of summary text ", len(summary.split(' ')))
    
    return summary, doc, len(rawdocs.split(' ')), len(summary.split(' '))











# calgoritma yang dipakai extrantion-based summarization, karena ringkasan dibuat dengan mengidentifikasi 
# dan mengekstrak kalimat-kalimat yang dianggap paling penting atau relevan dari teks asli.
# metodenya ini melibatkan pemberian skor pada setiap kalimat dan pemilihan kalimat-klaimat teratas berdasarkan skor tersebut 