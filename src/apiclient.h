#ifndef APICLIENT_H
#define APICLIENT_H

#include <QObject>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QString>
#include <QJsonArray>

class ApiClient : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString apiUrl READ apiUrl WRITE setApiUrl NOTIFY apiUrlChanged)
    Q_PROPERTY(bool loading READ loading NOTIFY loadingChanged)
    Q_PROPERTY(QString status READ status NOTIFY statusChanged)

public:
    explicit ApiClient(QObject *parent = nullptr);

    QString apiUrl() const { return m_apiUrl; }
    void setApiUrl(const QString &url);

    bool loading() const { return m_loading; }
    QString status() const { return m_status; }

    Q_INVOKABLE void search(const QString &sources, int maxAds,
                            double minPrice, double maxPrice,
                            const QString &brand, const QString &province);

signals:
    void resultsReceived(const QJsonArray &results);
    void searchFinished();
    void errorOccurred(const QString &error);
    void statusChanged(const QString &status);
    void loadingChanged(bool loading);
    void apiUrlChanged(const QString &url);

private slots:
    void onReplyFinished(QNetworkReply *reply);

private:
    QString m_apiUrl = "http://localhost:8000";
    bool m_loading = false;
    QString m_status;
    QNetworkAccessManager *m_manager;
};

#endif
