"""Test of the basics of dnstwist."""
import dnstwister.dnstwist.dnstwist as dnstwist


def test_generator_is_same_as_original():
    """Test the new fuzz iter is the same as the old system."""
    fuzzer = dnstwist.fuzz_domain('amazon.net')
    fuzzer.fuzz()
    original_results = sorted([r['domain-name']
                               for r
                               in fuzzer.domains])

    fuzzer = dnstwist.fuzz_domain('amazon.net')
    generator_results = sorted([r.domain
                                for r
                                in fuzzer.fuzz_iter(de_dupe=True)])

    missing_from_original = [d
                             for d
                             in generator_results
                             if d not in original_results]

    assert missing_from_original == []

    missing_from_generator = [d
                              for d
                              in original_results
                              if d not in generator_results]

    # The generator returns 3 less domains because those domains are actually
    # invalid.
    assert missing_from_generator == [u'amaz\u039fn.net', u'amaz\u041en.net', u'amaz\u0555n.net']


def test_small_domain_stats():
    """Test of the size of the results for a simple domain."""
    fuzzer = dnstwist.fuzz_domain('abc.com')
    fuzzer.fuzz()

    assert breakdown(fuzzer.domains) == {
        'Addition': 26,
        'Bitsquatting': 13,
        'Homoglyph': 27,
        'Hyphenation': 2,
        'Insertion': 8,
        'Omission': 3,
        'Original*': 1,
        'Repetition': 2,
        'Replacement': 14,
        'Subdomain': 2,
        'Transposition': 2,
        'Various': 4,
        'Vowel swap': 2
    }


def test_medium_domain_stats():
    """Test of the size of the results for a medium-length domain."""
    fuzzer = dnstwist.fuzz_domain('example.com')
    fuzzer.fuzz()

    assert breakdown(fuzzer.domains) == {
        'Addition': 26,
        'Bitsquatting': 33,
        'Homoglyph': 59,
        'Hyphenation': 6,
        'Insertion': 43,
        'Omission': 7,
        'Original*': 1,
        'Repetition': 3,
        'Replacement': 30,
        'Subdomain': 6,
        'Transposition': 6,
        'Various': 4,
        'Vowel swap': 6
    }


def test_medium_domain_with_subdomain_stats():
    """Test of the size of the results for a medium-length domain."""
    fuzzer = dnstwist.fuzz_domain('www.example.com')
    fuzzer.fuzz()

    assert breakdown(fuzzer.domains) == {
        'Addition': 26,
        'Bitsquatting': 49,
        'Homoglyph': 96,
        'Hyphenation': 8,
        'Insertion': 75,
        'Omission': 10,
        'Original*': 1,
        'Repetition': 4,
        'Replacement': 48,
        'Subdomain': 8,
        'Transposition': 8,
        'Various': 1,
        'Vowel swap': 6
    }


def test_crawler_massive_domain():
    """Test of the size of the results for a crawler monster domain."""
    fuzzer = dnstwist.fuzz_domain(
        'zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz.zzzzzzzzzzzzzzzzzzzzzzzzzppieo.com'
    )
    fuzzer.fuzz()

    assert breakdown(fuzzer.domains) == {
        'Addition': 26,
        'Bitsquatting': 288,
        'Homoglyph': 252,
        'Hyphenation': 29,
        'Insertion': 375,
        'Omission': 7,
        'Original*': 1,
        'Repetition': 4,
        'Replacement': 1077,
        'Subdomain': 91,
        'Transposition': 5,
        'Various': 1,
        'Vowel swap': 6
    }


def breakdown(result):
    return dict(
        [(f, len([d for d in result if d['fuzzer'] == f]))
         for f
         in set([d['fuzzer'] for d in result])]
     )


def test_unicode_fuzzing():
    """Test can fuzz and generate unicode."""
    unicode_domain = 'xn--domain.com'.decode('idna')

    fuzzer = dnstwist.fuzz_domain(unicode_domain)
    fuzzer.fuzz()

    assert sorted([d['domain-name'] for d in fuzzer.domains]) == [
        u'www-\u3bd9\u3bdc\u3bd9\u3bdf.com',
        u'www\u3bd9\u3bdc\u3bd9\u3bdf.com',
        u'ww\u3bd9\u3bdc\u3bd9\u3bdf.com',
        u'\u3bd9-\u3bdc\u3bd9\u3bdf.com',
        u'\u3bd9.\u3bdc\u3bd9\u3bdf.com',
        u'\u3bd9\u3bd9\u3bdc\u3bd9\u3bdf.com',
        u'\u3bd9\u3bd9\u3bdc\u3bdf.com',
        u'\u3bd9\u3bd9\u3bdf.com',
        u'\u3bd9\u3bdc-\u3bd9\u3bdf.com',
        u'\u3bd9\u3bdc.\u3bd9\u3bdf.com',
        u'\u3bd9\u3bdc\u3bd9-\u3bdf.com',
        u'\u3bd9\u3bdc\u3bd9.com',
        u'\u3bd9\u3bdc\u3bd9.\u3bdf.com',
        u'\u3bd9\u3bdc\u3bd9\u3bd9\u3bdf.com',
        u'\u3bd9\u3bdc\u3bd9\u3bdf.com',
        u'\u3bd9\u3bdc\u3bd9\u3bdfa.com',
        u'\u3bd9\u3bdc\u3bd9\u3bdfb.com',
        u'\u3bd9\u3bdc\u3bd9\u3bdfc.com',
        u'\u3bd9\u3bdc\u3bd9\u3bdfcom.com',
        u'\u3bd9\u3bdc\u3bd9\u3bdfd.com',
        u'\u3bd9\u3bdc\u3bd9\u3bdfe.com',
        u'\u3bd9\u3bdc\u3bd9\u3bdff.com',
        u'\u3bd9\u3bdc\u3bd9\u3bdfg.com',
        u'\u3bd9\u3bdc\u3bd9\u3bdfh.com',
        u'\u3bd9\u3bdc\u3bd9\u3bdfi.com',
        u'\u3bd9\u3bdc\u3bd9\u3bdfj.com',
        u'\u3bd9\u3bdc\u3bd9\u3bdfk.com',
        u'\u3bd9\u3bdc\u3bd9\u3bdfl.com',
        u'\u3bd9\u3bdc\u3bd9\u3bdfm.com',
        u'\u3bd9\u3bdc\u3bd9\u3bdfn.com',
        u'\u3bd9\u3bdc\u3bd9\u3bdfo.com',
        u'\u3bd9\u3bdc\u3bd9\u3bdfp.com',
        u'\u3bd9\u3bdc\u3bd9\u3bdfq.com',
        u'\u3bd9\u3bdc\u3bd9\u3bdfr.com',
        u'\u3bd9\u3bdc\u3bd9\u3bdfs.com',
        u'\u3bd9\u3bdc\u3bd9\u3bdft.com',
        u'\u3bd9\u3bdc\u3bd9\u3bdfu.com',
        u'\u3bd9\u3bdc\u3bd9\u3bdfv.com',
        u'\u3bd9\u3bdc\u3bd9\u3bdfw.com',
        u'\u3bd9\u3bdc\u3bd9\u3bdfx.com',
        u'\u3bd9\u3bdc\u3bd9\u3bdfy.com',
        u'\u3bd9\u3bdc\u3bd9\u3bdfz.com',
        u'\u3bd9\u3bdc\u3bd9\u3bdf\u3bdf.com',
        u'\u3bd9\u3bdc\u3bdc\u3bd9\u3bdf.com',
        u'\u3bd9\u3bdc\u3bdf.com',
        u'\u3bd9\u3bdc\u3bdf\u3bd9.com',
        u'\u3bdc\u3bd9\u3bd9\u3bdf.com',
        u'\u3bdc\u3bd9\u3bdf.com',
    ]


def test_top_level_domains_db_is_loaded():
    """The TLD database should be loaded."""
    assert dnstwist.DB_TLD


def test_basic_fuzz():
    """Test of the fuzzer.

    This'll be high-maintenance, but will help track changes over time.
    """
    fuzzer = dnstwist.fuzz_domain('www.example.com')
    fuzzer.fuzz()

    assert sorted(fuzzer.domains) == [
        {'domain-name': '2ww.example.com', 'fuzzer': 'Replacement'},
        {'domain-name': '3ww.example.com', 'fuzzer': 'Replacement'},
        {'domain-name': '7ww.example.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'aww.example.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'eww.example.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'gww.example.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'qww.example.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'sww.example.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'uww.example.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'vvvvvv.example.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': 'vvvvw.example.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': 'vvww.example.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': 'vww.example.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'w-ww.example.com', 'fuzzer': 'Hyphenation'},
        {'domain-name': 'w.example.com', 'fuzzer': 'Omission'},
        {'domain-name': 'w.ww.example.com', 'fuzzer': 'Subdomain'},
        {'domain-name': 'w2w.example.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'w2ww.example.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'w3w.example.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'w3ww.example.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'w7w.example.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'waw.example.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'waww.example.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'wew.example.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'weww.example.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'wgw.example.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'wqw.example.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'wqww.example.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'wsw.example.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'wsww.example.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'wuw.example.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'wvvvv.example.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': 'wvvw.example.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': 'wvw.example.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'ww-w.example.com', 'fuzzer': 'Hyphenation'},
        {'domain-name': 'ww.example.com', 'fuzzer': 'Omission'},
        {'domain-name': 'ww.w.example.com', 'fuzzer': 'Subdomain'},
        {'domain-name': 'ww.wexample.com', 'fuzzer': 'Transposition'},
        {'domain-name': 'ww2.example.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'ww2w.example.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'ww3.example.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'ww3w.example.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'ww7.example.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'wwa.example.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'wwaw.example.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'wwe.example.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'wwew.example.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'wwg.example.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'wwq.example.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'wwqw.example.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'wws.example.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'wwsw.example.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'wwu.example.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'wwv.example.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'wwvv.example.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': 'www.3example.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.3xample.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'www.4example.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.4xample.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'www.axample.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'www.dexample.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.dxample.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'www.e-xample.com', 'fuzzer': 'Hyphenation'},
        {'domain-name': 'www.e.xample.com', 'fuzzer': 'Subdomain'},
        {'domain-name': 'www.e3xample.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.e4xample.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.e8ample.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'www.eample.com', 'fuzzer': 'Omission'},
        {'domain-name': 'www.eaxmple.com', 'fuzzer': 'Transposition'},
        {'domain-name': 'www.ecample.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'www.ecxample.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.edample.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'www.edxample.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.eexample.com', 'fuzzer': 'Repetition'},
        {'domain-name': 'www.ehample.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'www.epample.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'www.erxample.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.esample.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'www.esxample.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.ewxample.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.ex-ample.com', 'fuzzer': 'Hyphenation'},
        {'domain-name': 'www.ex.ample.com', 'fuzzer': 'Subdomain'},
        {'domain-name': 'www.ex1ample.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.ex1mple.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'www.ex2ample.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.ex2mple.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'www.exa-mple.com', 'fuzzer': 'Hyphenation'},
        {'domain-name': 'www.exa-ple.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'www.exa.mple.com', 'fuzzer': 'Subdomain'},
        {'domain-name': 'www.exa1mple.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.exa2mple.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.exaample.com', 'fuzzer': 'Repetition'},
        {'domain-name': 'www.exaeple.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'www.exaiple.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'www.exajmple.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.exajple.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'www.exakmple.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.exakple.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'www.exalmple.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.exalple.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'www.exam-ple.com', 'fuzzer': 'Hyphenation'},
        {'domain-name': 'www.exam.ple.com', 'fuzzer': 'Subdomain'},
        {'domain-name': 'www.exam0le.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'www.exam0ple.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.examjple.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.examkple.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.examle.com', 'fuzzer': 'Omission'},
        {'domain-name': 'www.examlle.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'www.examlpe.com', 'fuzzer': 'Transposition'},
        {'domain-name': 'www.examlple.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.exammle.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'www.exammple.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.examnple.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.examole.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'www.examople.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.examp-le.com', 'fuzzer': 'Hyphenation'},
        {'domain-name': 'www.examp.le.com', 'fuzzer': 'Subdomain'},
        {'domain-name': 'www.examp0le.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.examp1e.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': 'www.exampde.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'www.exampe.com', 'fuzzer': 'Omission'},
        {'domain-name': 'www.exampel.com', 'fuzzer': 'Transposition'},
        {'domain-name': 'www.examphe.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'www.exampie.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': 'www.exampke.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'www.exampkle.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.exampl-e.com', 'fuzzer': 'Hyphenation'},
        {'domain-name': 'www.exampl.com', 'fuzzer': 'Omission'},
        {'domain-name': 'www.exampl.e.com', 'fuzzer': 'Subdomain'},
        {'domain-name': 'www.exampl3.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'www.exampl4.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'www.exampla.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'www.exampld.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'www.example.com', 'fuzzer': 'Original*'},
        {'domain-name': 'www.examplea.com', 'fuzzer': 'Addition'},
        {'domain-name': 'www.exampleb.com', 'fuzzer': 'Addition'},
        {'domain-name': 'www.examplec.com', 'fuzzer': 'Addition'},
        {'domain-name': 'www.examplecom.com', 'fuzzer': 'Various'},
        {'domain-name': 'www.exampled.com', 'fuzzer': 'Addition'},
        {'domain-name': 'www.examplee.com', 'fuzzer': 'Addition'},
        {'domain-name': 'www.examplef.com', 'fuzzer': 'Addition'},
        {'domain-name': 'www.exampleg.com', 'fuzzer': 'Addition'},
        {'domain-name': 'www.exampleh.com', 'fuzzer': 'Addition'},
        {'domain-name': 'www.examplei.com', 'fuzzer': 'Addition'},
        {'domain-name': 'www.examplej.com', 'fuzzer': 'Addition'},
        {'domain-name': 'www.examplek.com', 'fuzzer': 'Addition'},
        {'domain-name': 'www.examplel.com', 'fuzzer': 'Addition'},
        {'domain-name': 'www.examplem.com', 'fuzzer': 'Addition'},
        {'domain-name': 'www.examplen.com', 'fuzzer': 'Addition'},
        {'domain-name': 'www.exampleo.com', 'fuzzer': 'Addition'},
        {'domain-name': 'www.examplep.com', 'fuzzer': 'Addition'},
        {'domain-name': 'www.exampleq.com', 'fuzzer': 'Addition'},
        {'domain-name': 'www.exampler.com', 'fuzzer': 'Addition'},
        {'domain-name': 'www.examples.com', 'fuzzer': 'Addition'},
        {'domain-name': 'www.examplet.com', 'fuzzer': 'Addition'},
        {'domain-name': 'www.exampleu.com', 'fuzzer': 'Addition'},
        {'domain-name': 'www.examplev.com', 'fuzzer': 'Addition'},
        {'domain-name': 'www.examplew.com', 'fuzzer': 'Addition'},
        {'domain-name': 'www.examplex.com', 'fuzzer': 'Addition'},
        {'domain-name': 'www.exampley.com', 'fuzzer': 'Addition'},
        {'domain-name': 'www.examplez.com', 'fuzzer': 'Addition'},
        {'domain-name': 'www.examplg.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'www.exampli.com', 'fuzzer': 'Vowel swap'},
        {'domain-name': 'www.examplke.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.examplle.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.examplm.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'www.examplme.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.examplo.com', 'fuzzer': 'Vowel swap'},
        {'domain-name': 'www.examploe.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.examplpe.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.examplr.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'www.exampls.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'www.examplu.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'www.examplw.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'www.examplz.com', 'fuzzer': 'Replacement'},
        {'domain-name': u'www.exampl\xe9.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.exampl\xea.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.exampl\xeb.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.exampl\u0113.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.exampl\u0115.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.exampl\u0117.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.exampl\u0119.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.exampl\u011b.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.exampl\u03f5.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.exampl\u0435.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.exampl\u0454.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.exampl\u04bd.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.exampl\u1eb9.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': 'www.exampme.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'www.exampmle.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.exampne.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'www.exampoe.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'www.exampole.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.examppe.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'www.exampple.com', 'fuzzer': 'Insertion'},
        {'domain-name': u'www.examp\u0142e.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.examp\u026be.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': 'www.examqle.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'www.examrle.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'www.examtle.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'www.examxle.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': u'www.exam\xdele.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.exam\u01bfle.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.exam\u03c1le.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.exam\u03f7le.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.exam\u0440le.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': 'www.exanmple.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.exannple.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': 'www.exanple.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': 'www.exaople.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'www.exaple.com', 'fuzzer': 'Omission'},
        {'domain-name': 'www.exapmle.com', 'fuzzer': 'Transposition'},
        {'domain-name': 'www.exapmple.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.exapple.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'www.exaqmple.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.exarnple.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': 'www.exarrple.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': 'www.exasmple.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.exawmple.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.exaymple.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.exazmple.com', 'fuzzer': 'Insertion'},
        {'domain-name': u'www.exa\u0271ple.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.exa\u043cple.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.exa\u1d0dple.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.exa\u1e43ple.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': 'www.excample.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.excmple.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'www.exdample.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.exemple.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'www.eximple.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'www.exmaple.com', 'fuzzer': 'Transposition'},
        {'domain-name': 'www.exmple.com', 'fuzzer': 'Omission'},
        {'domain-name': 'www.exomple.com', 'fuzzer': 'Vowel swap'},
        {'domain-name': 'www.exqample.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.exqmple.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'www.exsample.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.exsmple.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'www.exumple.com', 'fuzzer': 'Vowel swap'},
        {'domain-name': 'www.exwample.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.exwmple.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'www.exxample.com', 'fuzzer': 'Repetition'},
        {'domain-name': 'www.exyample.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.exymple.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'www.exzample.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.exzmple.com', 'fuzzer': 'Replacement'},
        {'domain-name': u'www.ex\xe0mple.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.ex\xe1mple.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.ex\xe2mple.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.ex\xe3mple.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.ex\xe4mple.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.ex\xe5mple.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.ex\u0103mple.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.ex\u01cemple.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.ex\u0227mple.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.ex\u0251mple.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.ex\u0307ample.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.ex\u0430mple.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.ex\u04d3mple.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.ex\u1ea1mple.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': 'www.eyample.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'www.eyxample.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.ezample.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'www.ezxample.com', 'fuzzer': 'Insertion'},
        {'domain-name': u'www.e\u0445ample.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.e\u04b3ample.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': 'www.gxample.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'www.ixample.com', 'fuzzer': 'Vowel swap'},
        {'domain-name': 'www.mxample.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'www.oxample.com', 'fuzzer': 'Vowel swap'},
        {'domain-name': 'www.rexample.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.rxample.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'www.sexample.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.sxample.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'www.uxample.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'www.wexample.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.wxample.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'www.xample.com', 'fuzzer': 'Omission'},
        {'domain-name': 'www.xeample.com', 'fuzzer': 'Transposition'},
        {'domain-name': 'www.zexample.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www.zxample.com', 'fuzzer': 'Replacement'},
        {'domain-name': u'www.\xe9xample.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.\xe9xampl\xe9.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.\xeaxample.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.\xeaxampl\xea.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.\xebxample.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.\xebxampl\xeb.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.\u0113xample.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.\u0113xampl\u0113.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.\u0115xample.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.\u0115xampl\u0115.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.\u0117xample.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.\u0117xampl\u0117.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.\u0119xample.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.\u0119xampl\u0119.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.\u011bxample.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.\u011bxampl\u011b.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.\u03f5xample.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.\u03f5xampl\u03f5.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.\u0435xample.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.\u0435xampl\u0435.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.\u0454xample.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.\u0454xampl\u0454.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.\u04bdxample.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.\u04bdxampl\u04bd.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.\u1eb9xample.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'www.\u1eb9xampl\u1eb9.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': 'www2.example.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'www3.example.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'wwwa.example.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'wwwe.example.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'wwwe.xample.com', 'fuzzer': 'Transposition'},
        {'domain-name': 'wwwexample.com', 'fuzzer': 'Omission'},
        {'domain-name': 'wwwnexample.com', 'fuzzer': 'Bitsquatting'},
        {'domain-name': 'wwwq.example.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'wwws.example.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'wwww.example.com', 'fuzzer': 'Repetition'},
        {'domain-name': 'wwwx.example.com', 'fuzzer': 'Insertion'},
        {'domain-name': 'wwx.example.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'wwxw.example.com', 'fuzzer': 'Insertion'},
        {'domain-name': u'ww\u0461.example.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'ww\u051d.example.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'ww\u0561.example.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': 'wxw.example.com', 'fuzzer': 'Replacement'},
        {'domain-name': 'wxww.example.com', 'fuzzer': 'Insertion'},
        {'domain-name': u'w\u0461w.example.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'w\u0461\u0461.example.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'w\u051dw.example.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'w\u051d\u051d.example.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'w\u0561w.example.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'w\u0561\u0561.example.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': 'xww.example.com', 'fuzzer': 'Replacement'},
        {'domain-name': u'\u0461ww.example.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'\u0461\u0461w.example.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'\u0461\u0461\u0461.example.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'\u051dww.example.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'\u051d\u051dw.example.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'\u051d\u051d\u051d.example.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'\u0561ww.example.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'\u0561\u0561w.example.com', 'fuzzer': 'Homoglyph'},
        {'domain-name': u'\u0561\u0561\u0561.example.com', 'fuzzer': 'Homoglyph'}
    ]
