def personalization():
    """
    Generate event's vector representation, triggered on event created/updated
    Args:
        cloud_function_event (dict) : The dictionary with data specific to this type of event.
        - The `data` field contains the PubsubMessage message which is event's id.
    """


    import base64
    import json
    from sqlalchemy import func
    from db_model import (
        Event,
        EventDuration,
        DBSession,
        Tag,
        EventTag,
        EventVector
    )
    import numpy as np
    
    def tokenizer(text):
        return map(str.strip, text.split(','))

    event_id = 1


    # query event info 
    event_description = ''
    session = DBSession()
    try:
        query_event = (
            session.query(Event).filter(Event.id == event_id).scalar()
        )

        if query_event is not None:
            event_description = query_event.description

    except:
        session.rollback()
        raise
    finally:
        session.close()

    #  convert event description it into vector form 

    from sentence_transformers import SentenceTransformer
    sbert_model = SentenceTransformer('stsb-distilbert-base')
    sentence_embeddings = sbert_model.encode(event_description, show_progress_bar =True)

    # store event vector into db
    session = DBSession()
    try:
        event_vector = session.query(EventVector).filter_by(event_id = event_id).first()
        if not event_vector: # no bike in DB
            event_vector = EventVector(
                event_id = event_id,
                vector = sentence_embeddings.tolist()
            )
            session.add(event_vector)
        else:
            event_vector.vector = sentence_embeddings.tolist()
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

    # query all events, events_tag, events_vector from DB
    tags_ids = []
    session = DBSession()
    try:
        query_events_tags = session.query(EventTag).group_by(EventTag.event_id).values(func.array_agg(EventTag.tag_id))


        # TODO make sure order/amount of event tags and event vector is same

        for item in query_events_tags:
            delimiter = ','
            items = map(str, item[0])
            tags_ids.append(delimiter.join(items))

        events_vectors = session.query(EventVector).all()
        events_vectors = list(map(lambda event_vector: event_vector.vector, events_vectors))

    except:
        session.rollback()
        raise
    finally:
        session.close()

    # calculate tf-idf
    from sklearn.feature_extraction.text import TfidfVectorizer 

    vectorizer = TfidfVectorizer(tokenizer = tokenizer)
    tf_idf_sparce_array = vectorizer.fit_transform(tags_ids)
    tf_idf_feature = tf_idf_sparce_array.toarray()

    # calculate cosine similarity of tf-idf
    from sklearn.metrics.pairwise import linear_kernel
    cosine_sim_des_tags = linear_kernel(tf_idf_feature, tf_idf_feature)

    print(tags_ids, cosine_sim_des_tags[1])


    # calculate cosine similarity of event vector

    from sklearn.metrics.pairwise import cosine_similarity
    cosine_sim_des_descriptions = cosine_similarity(events_vectors, events_vectors)

    # combine tf-idf with event vector
    cosine_result = np.mean([cosine_sim_des_tags, cosine_sim_des_descriptions], axis = 0)

    # sort cosine similarity
    k_highest_score = []
    k = 50

    for item in cosine_result:
        index_of_score = np.argsort(item)[-k:]
        index_of_score = np.flip(index_of_score)
        result = np.array([index_of_score, item[index_of_score]]).T
        k_highest_score.append(result)

    k_highest_score = np.array(k_highest_score)

    # store cosine similarity


    # TODO store in somewhere
    print(k_highest_score)

personalization()
