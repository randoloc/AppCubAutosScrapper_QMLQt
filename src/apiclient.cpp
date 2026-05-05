#include "apiclient.h"
#include <QUrl>
#include <QUrlQuery>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>

ApiClient::ApiClient(QObject *parent)
    : QObject(parent)
    , m_manager(new QNetworkAccessManager(this))
{
}

void ApiClient::setApiUrl(const QString &url) {
    if (m_apiUrl != url) {
        m_apiUrl = url;
        emit apiUrlChanged(url);
    }
}

void ApiClient::search(const QString &sources, int maxAds,
                       double minPrice, double maxPrice,
                       const QString &brand, const QString &province)
{
    m_loading = true;
    emit loadingChanged(true);
    m_status = "Buscando...";
    emit statusChanged(m_status);

    QUrl url(m_apiUrl + "/api/search");
    QUrlQuery query;
    query.addQueryItem("sources", sources.isEmpty() ? "revolico,atrexport,chinautoscuba,cubamotor" : sources);
    query.addQueryItem("max_ads", QString::number(maxAds));
    if (minPrice > 0)
        query.addQueryItem("min_price", QString::number(minPrice, 'f', 0));
    if (maxPrice > 0)
        query.addQueryItem("max_price", QString::number(maxPrice, 'f', 0));
    if (!brand.isEmpty())
        query.addQueryItem("brand", brand);
    if (!province.isEmpty())
        query.addQueryItem("province", province);

    url.setQuery(query);

    QNetworkRequest request(url);
    request.setRawHeader("Accept", "application/json");
    request.setAttribute(QNetworkRequest::FollowRedirectsAttribute, true);

    QNetworkReply *reply = m_manager->get(request);
    connect(reply, &QNetworkReply::finished, this, [=]() {
        onReplyFinished(reply);
    });
}

void ApiClient::onReplyFinished(QNetworkReply *reply) {
    reply->deleteLater();

    if (reply->error() != QNetworkReply::NoError) {
        m_loading = false;
        emit loadingChanged(false);
        emit errorOccurred(reply->errorString());
        m_status = "Error";
        emit statusChanged(m_status);
        return;
    }

    QByteArray data = reply->readAll();
    QJsonDocument doc = QJsonDocument::fromJson(data);
    if (doc.isNull() || !doc.isObject()) {
        m_loading = false;
        emit loadingChanged(false);
        emit errorOccurred("Respuesta invalida del servidor");
        return;
    }

    QJsonObject obj = doc.object();
    int count = obj.value("count").toInt();
    bool cached = obj.value("cached").toBool();
    QJsonArray results = obj.value("results").toArray();

    emit resultsReceived(results);
    m_status = (cached ? "[cache] " : "") + QString::number(count) + " resultados";
    emit statusChanged(m_status);

    emit searchFinished();

    m_loading = false;
    emit loadingChanged(false);
}
