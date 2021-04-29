def personalization(cloud_function_event):
    """
    Generate event's vector representation, triggered on event created/updated
    Args:
        cloud_function_event (dict) : The dictionary with data specific to this type of event.
        - The `data` field contains the PubsubMessage message which is event's id.
    """

    import base64
    import json
    from db_model import (
        Event,
        EventDuration,
        DBSession,
        Tag,
        EventTag,
        EventVector
    )

    if 'data' in cloud_function_event:
        message = base64.b64decode(cloud_function_event['data']).decode('utf-8')
        message_dict = json.loads(message)
        event_id = int(message_dict['data'])

        # query event info 
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
        sbert_model = SentenceTransformer('stsb-roberta-large')
        sentence_embeddings = sbert_model.encode(event_description, show_progress_bar =True)

        # store event vector into db
        session = DBSession()
        try:
            event_vector = EventVector(
                event_id = event_id,
                vector = sentence_embeddings
            )
            session.add(event_vector)
            session.commit()

        except:
            session.rollback()
            raise
        finally:
            session.close()


        # query all events, events_tag, events_vector from DB

        session = DBSession()
        try:
            # query_tags = session.query(Tag).all()
            # tags_dict = dict(map(operator.itemgetter('id','name'), query_tags))
            
            
            query_events_tags = session.query(EventTag).all()
    
            # events_tags = map(lambda event: tags_dict[event.tag_id], query_events_tags)

            # data = map(
            #     lambda event: common.Event(
            #         id=event.id,
            #         organization_id=event.organization_id,
            #         location_id=getInt32Value(event.location_id),
            #         description=event.description,
            #         name=event.name,
            #         cover_image_url=getStringValue(event.cover_image_url),
            #         cover_image_hash=getStringValue(event.cover_image_hash),
            #         poster_image_url=getStringValue(event.poster_image_url),
            #         poster_image_hash=getStringValue(event.poster_image_hash),
            #         profile_image_url=getStringValue(event.profile_image_url),
            #         profile_image_hash=getStringValue(event.profile_image_hash),
            #         attendee_limit=event.attendee_limit,
            #         contact=getStringValue(event.contact),
            #         registration_due_date=getTimeStamp(event.registration_due_date),
            #     ),
            #     query_events,
            # )
            return participant_service.EventsResponse(event=data)
        except:
            session.rollback()
            raise
        finally:
            session.close()
        events
        events_tags
        events_vectors

        # calculate tf-idf

        from sklearn.feature_extraction.text import TfidfVectorizer 
 
        vectorizer = TfidfVectorizer(tokenizer = tokenizer)
        tf_idf_sparce_array = vectorizer.fit_transform(events_tags)
        tf_idf_feature = tf_idf_sparce_array.toarray()

        # calculate cosine similarity of tf-idf

        from sklearn.metrics.pairwise import linear_kernel
        cosine_sim_des_tags = linear_kernel(tf_idf_feature, tf_idf_feature)

        # calculate cosine similarity of event vector

        from sklearn.metrics.pairwise import cosine_similarity
        cosine_sim_des_descriptions = cosine_similarity(events_vectors, events_vectors)

        # combine tf-idf with event vector
        cosine_result = np.mean([cosine_sim_des_descriptions, cosine_sim_des_tags], axis = 0)

        # sort cosine similarity
        k_highest_score = []
        k = 50

        for item in test:
            index_of_score = np.argsort(item)[-k:]
            index_of_score = np.flip(index_of_score)
            result = np.array([index_of_score, item[index_of_score]]).T
            k_highest_score.append(result)

        k_highest_score = np.array(k_highest_score)

        # store cosine similarity

        k_highest_score


        result = fib(int(message_dict['data']))
        print(str(result))
